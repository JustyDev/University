import { Controller, Post, Body, Get, Param } from '@nestjs/common';
import { ParserService } from './parser.service';
import { ParseRequestDto } from './dto/parse-request.dto';
import { ParseResultDto } from './dto/parse-result.dto';

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
}
