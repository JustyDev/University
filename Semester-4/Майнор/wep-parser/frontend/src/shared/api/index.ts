import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000',
});

export interface ParseResultDto {
  _id: string;
  urls: string[];
  results: Array<{
    url: string;
    status_code: number;
    status: 'failed' | 'success';
    data?: {
      textContent: string[];
      h1: string[]
      h2: string[]
      h3: string[]
      h4: string[]
      h5: string[]
      h6: string[]
      images: string[];
      internalLinks: string[];
      externalLinks: string[];
      title?: string;
      description?: string;
      keywords?: string[];
    };
    error?: string;
  }>;
  createdAt: string;
  updatedAt: string;
}
