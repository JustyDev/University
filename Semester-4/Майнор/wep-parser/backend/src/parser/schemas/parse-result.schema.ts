import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema({ timestamps: true })
export class ParseResult extends Document {
  @Prop({ required: true })
  requestId: string;

  @Prop({ required: true })
  urls: string[];

  @Prop({ required: true, type: [Object] })
  results: Array<{
    url: string;
    status_code: number;
    status: 'failed' | 'success';
    data?: {
      title?: string;
      description?: string;
      textContent: string[];
      headers: Array<{ tag: string; text: string }>;
      images: string[];
      internalLinks: string[];
      externalLinks: string[];
      html: string;
    };
    error?: string;
  }>;
}

export const ParseResultSchema = SchemaFactory.createForClass(ParseResult);
