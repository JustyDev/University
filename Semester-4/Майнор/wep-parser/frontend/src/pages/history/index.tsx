import {useUnit} from 'effector-react';
import {historyModel} from './model';
import {useEffect} from "react";
import {Loader} from "@shared/ui";
import {PageLayout} from "@shared/ui/page-layout";

import s from './history.module.css'
import {HistoryCard} from "./ui/history-card";

export function HistoryPage() {
  const {history, isLoading} = useUnit({
    history: historyModel.$history,
    isLoading: historyModel.$isLoading,
  });

  useEffect(() => {
    historyModel.fetchHistoryFx()
  }, []);

  return (
    <PageLayout className={s.page}>
      <h1 className={s.title}>История парсинга</h1>
      <div className={s.listContainer}>
        {isLoading && <Loader label='Получение истории...'/>}

        {!isLoading && history.map((item) => (
          <HistoryCard key={item._id} item={item}/>
        ))}
      </div>
    </PageLayout>
  );
}
