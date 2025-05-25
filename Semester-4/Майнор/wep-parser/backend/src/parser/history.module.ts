import { Module } from '@nestjs/common';
import { HistoryController } from './history.controller';
import { MongooseModule } from '@nestjs/mongoose';
import { ParseResult, ParseResultSchema } from './schemas/parse-result.schema';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: ParseResult.name, schema: ParseResultSchema }
    ])
  ],
  controllers: [HistoryController]
})
export class HistoryModule {}
