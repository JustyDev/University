import { createEffect, createEvent, createStore, sample } from 'effector';
import { createGate } from 'effector-react';
import axios from 'axios';

// Types
export interface UrlInput {
  id: string;
  value: string;
}

export interface ParserSettings {
  depth: number;
  extractLinks: boolean;
  extractTitles: boolean;
  extractImages: boolean;
  extractDescriptions: boolean;
  extractTextContent: boolean;
  extractInternalLinks: boolean;
  extractExternalLinks: boolean;
  extractH1: boolean;
  extractH2: boolean;
  extractH3: boolean;
  extractH4: boolean;
  extractH5: boolean;
  extractH6: boolean;
}

// Events
export const addUrlInput = createEvent();
export const updateUrlInput = createEvent<{ id: string; value: string }>();
export const removeUrlInput = createEvent<string>();
export const parseUrls = createEvent<{urls: string[], settings: ParserSettings}>();
export const updateParserSettings = createEvent<Partial<ParserSettings>>();

// Stores
export const $urlInputs = createStore<UrlInput[]>([{ id: '1', value: '' }]);
export interface ParseData {
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
}

export interface ParseResult {
  _id: string;
  urls: string[];
  results: Array<{
    url: string;
    status_code: number;
    status: 'failed' | 'success';
    data?: ParseData;
    error?: string;
  }>;
  createdAt: Date;
  updatedAt: Date;
}

export const $results = createStore<ParseResult | null>(null);
export const $isLoading = createStore(false);
export const $parsingError = createStore<string | null>(null);
export const $parserSettings = createStore<ParserSettings>({
  depth: 1,
  extractLinks: true,
  extractTitles: true,
  extractImages: true,
  extractDescriptions: true,
  extractTextContent: true,
  extractInternalLinks: true,
  extractExternalLinks: true,
  extractH1: true,
  extractH2: true,
  extractH3: true,
  extractH4: true,
  extractH5: true,
  extractH6: true
});

// Effects
export const parseUrlsFx = createEffect<{urls: string[], settings: ParserSettings}, ParseResult>(async (params) => {
  const { urls, settings } = params;
  
  if (!urls.length) {
    throw new Error('Введите хотя бы один URL');
  }

  const response = await axios.post('http://localhost:3000/parser', {
    urls,
    options: settings
  });
  
  return response.data;
});

export const getResultById = async (id: string) => {
  const response = await axios.get(`http://localhost:3000/parser/${id}`);
  return response.data;
};

// Logic
$urlInputs
  .on(addUrlInput, (state) => [...state, { id: Date.now().toString(), value: '' }])
  .on(updateUrlInput, (state, { id, value }) => 
    state.map(input => input.id === id ? { ...input, value } : input)
  )
  .on(removeUrlInput, (state, id) => 
    state.filter(input => input.id !== id)
  );

$parserSettings
  .on(updateParserSettings, (state, payload) => ({
    ...state,
    ...payload
  }));

$results
  .on(parseUrlsFx.doneData, (_, results) => results)
  .reset(parseUrls);

$isLoading
  .on(parseUrlsFx, () => true)
  .on(parseUrlsFx.finally, () => false);

$parsingError
  .on(parseUrlsFx.failData, (_, error) => error.message)
  .reset(parseUrlsFx);

// Navigation
export const ResultsGate = createGate();

sample({
  clock: parseUrls,
  fn: (params) => ({ urls: params.urls, settings: params.settings }),
  target: parseUrlsFx
});

sample({
  clock: parseUrlsFx.done,
  target: ResultsGate.open
});
