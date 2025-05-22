import { ApiProperty } from '@nestjs/swagger';

export class ParseDataDto {
  @ApiProperty()
  title?: string;

  @ApiProperty()
  description?: string;

  @ApiProperty()
  textContent: string[];

  @ApiProperty()
  headers: Array<{
    tag: 'h1' | 'h2' | 'h3';
    text: string;
  }>;

  @ApiProperty()
  images: string[];

  @ApiProperty()
  internalLinks: string[];

  @ApiProperty()
  externalLinks: string[];

  @ApiProperty()
  html: string;
}

export class ParseResultDto {
  @ApiProperty()
  requestId: string;

  @ApiProperty()
  urls: string[];

  @ApiProperty({ type: [Object] })
  results: Array<{
    url: string;
    status_code: number;
    status: 'failed' | 'success';
    data?: ParseDataDto;
    error?: string;
  }>;
}
