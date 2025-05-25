import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { ParseResult, ParseResultSchema } from './parser/schemas/parse-result.schema';
import { ParserController } from './parser/parser.controller';
import { ParserService } from './parser/parser.service';
import { HistoryModule } from './parser/history.module';

@Module({
  imports: [
    MongooseModule.forRoot('mongodb://localhost:27017/parser'),
    MongooseModule.forFeature([{ name: ParseResult.name, schema: ParseResultSchema }]),
    HistoryModule,
  ],
  controllers: [ParserController],
  providers: [ParserService],
})
export class AppModule {}
