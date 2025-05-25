import {HttpException, Injectable, Logger} from '@nestjs/common';
import {Model} from 'mongoose';
import {InjectModel} from '@nestjs/mongoose';
import {ParseResult} from './schemas/parse-result.schema';
import {ParseOptionsDto, ParseRequestDto} from './dto/parse-request.dto';
import {ParseDataDto, ParseResultDto} from './dto/parse-result.dto';
import * as cheerio from 'cheerio';
import * as puppeteer from 'puppeteer';

@Injectable()
export class ParserService {
  constructor(
    @InjectModel(ParseResult.name)
    private readonly parseResultModel: Model<ParseResult>,
  ) {
  }

  private readonly logger = new Logger(ParserService.name);

  async parse(parseRequest: ParseRequestDto): Promise<ParseResult> {
    const browser = await puppeteer.launch();

    const urls = parseRequest.urls.map((url) => {
      if (url.startsWith('http')) return;

      return 'https://' + url;
    })

    if (!urls.length) {
      throw new HttpException('No urls specified', 500);
    }

    try {
      const results = await this.processUrlsWithQueue(
        browser,
        urls,
        parseRequest.options
      );

      return await this.parseResultModel.create({
        urls,
        results
      });
    } finally {
      await browser.close();
    }
  }

  async getResults(id: string): Promise<ParseResultDto> {
    const result = await this.parseResultModel.findById(id).lean<ParseResult>();
    if (!result) {
      throw new Error('Result not found');
    }
    return {
      _id: result._id.toString(),
      urls: result.urls,
      results: result.results,
      createdAt: new Date(result.createdAt),
      updatedAt: new Date(result.updatedAt)
    };
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
    const queue: { url: string; depth: number; parentUrl?: string }[] = [];
    const processedUrls = new Set<string>();
    const results: Array<{
      url: string;
      status_code: number;
      status: 'failed' | 'success';
      data?: ParseDataDto;
      error?: string;
    }> = [];

    urls.forEach(url => queue.push({url, depth: 1}));

    while (queue.length > 0) {
      const {url, depth, parentUrl} = queue.shift()!;
      this.logger.log(`Process url: ${url}`);

      if (processedUrls.has(url)) {
        this.logger.log(`Skipping already processed URL: ${url}`);
        continue;
      }

      const pageData = await this.fetchPageData(browser, url, depth, options, parentUrl);
      results.push(pageData);
      processedUrls.add(url);

      if (depth < options.depth && pageData.status === 'success' && pageData.data) {
        const allLinks = [...pageData.data.internalLinks, ...pageData.data.externalLinks];

        for (const link of allLinks) {
          if (processedUrls.has(link)) continue;
          if (!link.startsWith('http')) continue;

          queue.push({
            url: link,
            depth: depth + 1,
            parentUrl: url
          });
        }
      }
    }

    return results;
  }

  private async fetchPageData(
    browser: puppeteer.Browser,
    url: string,
    depth: number,
    options: ParseOptionsDto,
    parentUrl?: string
  ): Promise<{
    url: string;
    status_code: number;
    depth: number;
    status: 'failed' | 'success';
    data?: ParseDataDto;
    error?: string;
    parent_url?: string;
  }> {
    const {html, status, error} = await this.fetchHtml(browser, url);

    if (status >= 400 || error) {
      return {
        url,
        status_code: status,
        status: 'failed',
        parent_url: parentUrl,
        depth: depth,
        error: error || `HTTP Error ${status}`
      };
    }

    const $ = cheerio.load(html);
    const parseData: ParseDataDto = {
      textContent: options.extractTextContent ? this.extractTextContent(html) : [],
      h1: options.extractH1 ? this.extractHeaders(html, 'h1') : [],
      h2: options.extractH2 ? this.extractHeaders(html, 'h2') : [],
      h3: options.extractH3 ? this.extractHeaders(html, 'h3') : [],
      h4: options.extractH4 ? this.extractHeaders(html, 'h4') : [],
      h5: options.extractH5 ? this.extractHeaders(html, 'h5') : [],
      h6: options.extractH6 ? this.extractHeaders(html, 'h6') : [],
      images: options.extractImages ? await this.extractImages(html) : [],
      internalLinks: [],
      externalLinks: []
    };

    if (options.extractDescriptions) {
      parseData.title = $('title').text();
      parseData.description = $('meta[name="description"]').attr('content');
      parseData.keywords = this.extractKeywords(html);
    }

    if (options.extractH1) parseData.h1 = this.extractHeaders(html, 'h1');
    if (options.extractH2) parseData.h2 = this.extractHeaders(html, 'h2');
    if (options.extractH3) parseData.h3 = this.extractHeaders(html, 'h3');
    if (options.extractH4) parseData.h4 = this.extractHeaders(html, 'h4');
    if (options.extractH5) parseData.h5 = this.extractHeaders(html, 'h5');
    if (options.extractH6) parseData.h6 = this.extractHeaders(html, 'h6');

    if (options.extractImages) {
      parseData.images = await this.extractImages(html);
    }

    const allLinks = await this.extractLinks(html);
    const {internalLinks, externalLinks} = this.categorizeLinks(allLinks, url);

    if (options.extractInternalLinks) {
      parseData.internalLinks = internalLinks;
    }
    if (options.extractExternalLinks) {
      parseData.externalLinks = externalLinks;
    }

    return {
      url,
      status_code: status,
      status: 'success',
      depth: depth,
      data: parseData,
      parent_url: parentUrl
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

  private isValidUrl(url: string): boolean {
    try {
      // Skip empty, anchor-only or javascript: links
      if (!url || url.startsWith('#') || url.startsWith('javascript:')) {
        return false;
      }

      // Basic URL validation
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  private async extractLinks(html: string): Promise<string[]> {
    const links = new Set<string>();
    const regex = /<a[^>]+href="([^"]*)"[^>]*>/g;
    let match: RegExpExecArray | null;

    while ((match = regex.exec(html)) !== null) {
      if (match[1] && this.isValidUrl(match[1])) {
        links.add(match[1].trim());
      }
    }

    return Array.from(links);
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

      // Add https:// if no protocol is specified
      if (!url.includes('://') && !url.startsWith('/')) {
        url = `https://${url}`;
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

    return {internalLinks, externalLinks};
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

  private extractHeaders(html: string, tag: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6'): string[] {
    const $ = cheerio.load(html);
    return $(tag).map((_, el) => $(el).text().trim()).get();
  }

  private extractKeywords(html: string): string[] {
    const $ = cheerio.load(html);
    const keywords = $('meta[name="keywords"]').attr('content');
    return keywords ? keywords.split(',').map(k => k.trim()) : [];
  }
}
