import { ApiProperty } from '@nestjs/swagger';

export class ParseDataDto {
  @ApiProperty()
  title?: string;

  @ApiProperty()
  description?: string;

  @ApiProperty()
  keywords?: string[];

  @ApiProperty()
  textContent: string[];

  @ApiProperty()
  h1: string[];

  @ApiProperty()
  h2: string[];

  @ApiProperty()
  h3: string[];

  @ApiProperty()
  h4: string[];

  @ApiProperty()
  h5: string[];

  @ApiProperty()
  h6: string[];

  @ApiProperty()
  images: string[];

  @ApiProperty()
  internalLinks: string[];

  @ApiProperty()
  externalLinks: string[];
}

export class ParseResultDto {
  @ApiProperty()
  _id: string;

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

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;
}
