export class ParseOptionsDto {
  depth: number = 1;
  extractInternalLinks: boolean = true;
  extractExternalLinks: boolean = true;
  extractH1: boolean = true;
  extractH2: boolean = true;
  extractH3: boolean = true;
  extractH4: boolean = true;
  extractH5: boolean = true;
  extractH6: boolean = true;
  extractImages: boolean = true;
  extractDescriptions: boolean = true;
  extractTextContent: boolean = true;
}

export class ParseRequestDto {
  urls: string[];
  options: ParseOptionsDto;
}
