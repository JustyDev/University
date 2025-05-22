import { Injectable, Logger, Inject } from '@nestjs/common';
import { Model } from 'mongoose';
import { InjectModel } from '@nestjs/mongoose';
import { ParseResult } from './schemas/parse-result.schema';
import { ParseRequestDto, ParseOptionsDto } from './dto/parse-request.dto';
import { ParseResultDto, ParseDataDto } from './dto/parse-result.dto';
import * as cheerio from 'cheerio';
import * as puppeteer from 'puppeteer';

@Injectable()
export class ParserService {
  constructor(
    @InjectModel(ParseResult.name)
    private readonly parseResultModel: Model<ParseResult>,
  ) {}
  private readonly logger = new Logger(ParserService.name);

  async parse(parseRequest: ParseRequestDto): Promise<ParseResultDto> {
    const browser = await puppeteer.launch();
    try {
      const results = await this.processUrlsWithQueue(
        browser,
        parseRequest.urls,
        parseRequest.options
      );
      
      // Save results to MongoDB
      const requestId = Date.now().toString();
      const parseResult = {
        requestId,
        urls: parseRequest.urls,
        results
      };
      await this.parseResultModel.create(parseResult);
      
      return parseResult;
    } finally {
      await browser.close();
    }
  }

  private async processUrlsWithQueue(
    browser: puppeteer.Browser,
    urls: string[],
    options: ParseOptionsDto
  ): Promise<Array<{
    url: string;
    status_code: number;
    status: 'failed' | 'success';
    data?: ParseDataDto;
    error?: string;
  }>> {
    const queue: {url: string; depth: number; parentUrl?: string}[] = [];
    const processedUrls = new Set<string>();
    const results: Array<{
      url: string;
      status_code: number;
      status: 'failed' | 'success';
      data?: ParseDataDto;
      error?: string;
    }> = [];

    // Initialize queue with starting URLs
    urls.forEach(url => queue.push({url, depth: 0}));

    while (queue.length > 0) {
      const {url, depth, parentUrl} = queue.shift()!;

      this.logger.log(`Process url: ${url}`);

      if (processedUrls.has(url)) {
        this.logger.log(`Skipping already processed URL: ${url}`);
        continue;
      }

      const pageData = await this.fetchPageData(browser, url, depth, parentUrl);
      results.push(pageData);
      processedUrls.add(url);

      // Add child links to queue if not at max depth
      if (depth < options.depth && pageData.status === 'success' && pageData.data) {
        for (const link of pageData.data.internalLinks) {
          if (!processedUrls.has(link)) {
            queue.push({
              url: link,
              depth: depth + 1,
              parentUrl: url
            });
          }
        }
      }
    }

    return results;
  }

  private async fetchPageData(
    browser: puppeteer.Browser,
    url: string,
    depth: number,
    parentUrl?: string
  ): Promise<{
    url: string;
    status_code: number;
    status: 'failed' | 'success';
    data?: ParseDataDto;
    error?: string;
  }> {
    const { html, status, error } = await this.fetchHtml(browser, url);
    
    if (status >= 400 || error) {
      return {
        url,
        status_code: status,
        status: 'failed',
        error: error || `HTTP Error ${status}`
      };
    }

    const $ = cheerio.load(html);
    const parseData: ParseDataDto = {
      title: $('title').text(),
      description: $('meta[name="description"]').attr('content'),
      textContent: this.extractTextContent(html),
      headers: this.extractHeaders(html),
      images: await this.extractImages(html),
      internalLinks: [],
      externalLinks: [],
      html
    };

    const allLinks = await this.extractLinks(html);
    const { internalLinks, externalLinks } = this.categorizeLinks(allLinks, url);
    parseData.internalLinks = internalLinks;
    parseData.externalLinks = externalLinks;

    return {
      url,
      status_code: status,
      status: 'success',
      data: parseData
    };
  }

  private async fetchHtml(browser: puppeteer.Browser, url: string): Promise<{
    html: string;
    status: number;
    error?: string;
  }> {
    const page = await browser.newPage();
    try {
      const response = await page.goto(url, {
        waitUntil: 'networkidle2',
        timeout: 10000
      });

      if (!response) {
        return {
          html: '',
          status: 500,
          error: 'No response from server'
        };
      }

      const status = response.status();
      if (status >= 400) {
        return {
          html: '',
          status,
          error: `HTTP Error ${status}`
        };
      }

      return {
        html: await page.content(),
        status
      };
    } catch (error) {
      return {
        html: '',
        status: 500,
        error: error.message
      };
    } finally {
      await page.close();
    }
  }

  private async extractLinks(html: string): Promise<string[]> {
    const links: string[] = [];
    const regex = /<a[^>]+href="([^"]*)"[^>]*>/g;
    let match: RegExpExecArray | null;
    while ((match = regex.exec(html)) !== null) {
      if (match[1]) links.push(match[1]);
    }
    return links;
  }

  private async extractImages(html: string): Promise<string[]> {
    const images: string[] = [];
    const regex = /<img[^>]+src="([^"]*)"[^>]*>/g;
    let match: RegExpExecArray | null;
    while ((match = regex.exec(html)) !== null) {
      if (match[1]) images.push(match[1]);
    }
    return images;
  }

  private normalizeUrl(url: string, baseUrl: string): string {
    try {
      if (url.startsWith('http://') || url.startsWith('https://')) {
        return url;
      }
      const base = new URL(baseUrl);
      return new URL(url, base.origin).href;
    } catch (e) {
      return url;
    }
  }

  private categorizeLinks(links: string[], baseUrl: string): { internalLinks: string[]; externalLinks: string[] } {
    const internalLinks: string[] = [];
    const externalLinks: string[] = [];

    links.forEach(link => {
      const normalized = this.normalizeUrl(link, baseUrl);
      if (normalized.startsWith('http://') || normalized.startsWith('https://')) {
        if (new URL(normalized).hostname === new URL(baseUrl).hostname) {
          internalLinks.push(normalized);
        } else {
          externalLinks.push(normalized);
        }
      }
    });

    return { internalLinks, externalLinks };
  }

  private extractTextContent(html: string): string[] {
    const $ = cheerio.load(html);
    $('script, style, noscript, iframe, svg').remove();
    const textBlocks: string[] = [];
    
    $('body *').each((_, el) => {
      if ($(el).children().length === 0) {
        const text = $(el).text().trim();
        if (text) {
          textBlocks.push(text);
        }
      }
    });
    
    return textBlocks;
  }

  private extractHeaders(html: string): Array<{tag: 'h1'|'h2'|'h3', text: string}> {
    const $ = cheerio.load(html);
    const headers: Array<{tag: 'h1'|'h2'|'h3', text: string}> = [];
    
    $('h1, h2, h3').each((_, el) => {
      const tag = el.tagName.toLowerCase() as 'h1'|'h2'|'h3';
      headers.push({
        tag,
        text: $(el).text().trim()
      });
    });
    
    return headers;
  }
}
