import { Controller, Post, Body } from '@nestjs/common';
import { ParserService } from './parser.service';
import { ParseRequestDto } from './dto/parse-request.dto';
import { ParseResultDto } from './dto/parse-result.dto';

@Controller('parser')
export class ParserController {
  constructor(private readonly parserService: ParserService) {}

  @Post()
  async parse(@Body() parseRequest: ParseRequestDto): Promise<ParseResultDto> {
    return this.parserService.parse(parseRequest);
  }
}
