import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { ParseResult, ParseResultSchema } from './parser/schemas/parse-result.schema';
import { ParserController } from './parser/parser.controller';
import { ParserService } from './parser/parser.service';

@Module({
  imports: [
    MongooseModule.forRoot('mongodb://localhost:27017/parser'),
    MongooseModule.forFeature([{ name: ParseResult.name, schema: ParseResultSchema }]),
  ],
  controllers: [ParserController],
  providers: [ParserService],
})
export class AppModule {}
