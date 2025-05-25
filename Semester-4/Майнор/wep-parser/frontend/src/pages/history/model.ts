import {createEffect, createStore} from 'effector';
import type {ParseResultDto} from '@/shared/api';
import {api} from '@/shared/api';

export type HistoryItem = ParseResultDto;

export const historyModel = {
  $history: createStore<HistoryItem[]>([]),
  $isLoading: createStore(false),

  fetchHistoryFx: createEffect(async () => {
    const {data} = await api.get<HistoryItem[]>('/history');
    return data;
  }),
};

historyModel.$history
  .on(historyModel.fetchHistoryFx.doneData, (_, data) => data);

historyModel.$isLoading
  .on(historyModel.fetchHistoryFx.pending, (_, pending) => pending);
