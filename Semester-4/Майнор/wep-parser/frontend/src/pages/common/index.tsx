import {UrlInputList} from '@/features/url-input-list';

import s from './common.module.css'
import {Loader, MainBackground} from "@shared/ui";
import {useUnit} from "effector-react/effector-react.mjs";
import {$isLoading, parseUrlsFx} from "@shared/model/parser.ts";
import {useNavigate} from "react-router-dom";
import {useEffect} from "react";

export function CommonPage() {

  const isLoading = useUnit($isLoading)

  const navigate = useNavigate()

  useEffect(() => {
    parseUrlsFx.doneData.watch((res) => {
      navigate(`/result/${res.id}`)
    })
  }, []);

  return (
    <div className={s.wrapper}>
      <MainBackground/>

      {isLoading && <Loader/>}

      {!isLoading && <main className={s.content}>

          <h1 className={s.title}>Что изучить сегодня?</h1>

          <UrlInputList/>

          <p className={s.desc}>Укажите ссылки на сайты и выберите, какую информацию хотите получить, а мы попробуем её
              собрать и
              подготовить для вас</p>

      </main>}
    </div>
  );
}
