export class ParseOptionsDto {
  depth: number = 0;
  extractLinks: boolean = true;
  extractTitles: boolean = true;
  extractImages: boolean = true;
  extractDescriptions: boolean = true;
  extractTextContent: boolean = true;
}

export class ParseRequestDto {
  urls: string[];
  options: ParseOptionsDto;
}
