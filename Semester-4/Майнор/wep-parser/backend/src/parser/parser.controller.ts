import { Controller, Post, Body, Get, Param, Res, Header } from '@nestjs/common';
import { ParserService } from './parser.service';
import { ParseRequestDto } from './dto/parse-request.dto';
import { ParseResultDto } from './dto/parse-result.dto';
import * as yaml from 'js-yaml';
import { js2xml } from 'xml-js';

@Controller('parser')
export class ParserController {
  constructor(private readonly parserService: ParserService) {}

  @Post()
  async parse(@Body() parseRequest: ParseRequestDto): Promise<{ id: string }> {
    const result = await this.parserService.parse(parseRequest);
    return { id: result._id.toString() };
  }

  @Get(':id')
  async getResults(@Param('id') id: string): Promise<ParseResultDto> {
    return this.parserService.getResults(id);
  }

  @Get(':id/downloadJson')
  @Header('Content-Type', 'application/json')
  @Header('Content-Disposition', 'attachment; filename="result.json"')
  async downloadJson(@Param('id') id: string, @Res() res) {
    const result = await this.parserService.getResults(id);
    res.send(JSON.stringify(result, null, 2));
  }

  @Get(':id/downloadYaml')
  @Header('Content-Type', 'application/yaml')
  @Header('Content-Disposition', 'attachment; filename="result.yaml"')
  async downloadYaml(@Param('id') id: string, @Res() res) {
    const result = await this.parserService.getResults(id);
    res.send(yaml.dump(result));
  }

  @Get(':id/downloadXml')
  @Header('Content-Type', 'application/xml')
  @Header('Content-Disposition', 'attachment; filename="result.xml"')
  async downloadXml(@Param('id') id: string, @Res() res) {
    const result = await this.parserService.getResults(id);
    res.send(js2xml(result, {compact: true, spaces: 2}));
  }
}
