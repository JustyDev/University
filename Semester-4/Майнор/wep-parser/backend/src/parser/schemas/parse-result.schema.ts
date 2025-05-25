import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema({ timestamps: true })
export class ParseResult extends Document {
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
      keywords?: string[];
      textContent: string[];
      h1: string[];
      h2: string[];
      h3: string[];
      h4: string[];
      h5: string[];
      h6: string[];
      images: string[];
      internalLinks: string[];
      externalLinks: string[];
    };
    error?: string;
  }>;

  createdAt: Date;
  updatedAt: Date;
}

export const ParseResultSchema = SchemaFactory.createForClass(ParseResult);
