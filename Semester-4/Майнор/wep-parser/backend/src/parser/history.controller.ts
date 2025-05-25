import { Controller, Get } from '@nestjs/common';
import { ParseResult } from './schemas/parse-result.schema';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';

@Controller('history')
export class HistoryController {
  constructor(
    @InjectModel(ParseResult.name)
    private readonly parseResultModel: Model<ParseResult>,
  ) {}

  @Get()
  async getAllHistory() {
    return this.parseResultModel
      .find()
      .sort({ createdAt: -1 })
      .lean()
      .exec();
  }
}
