import {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';
import {getResultById} from '@/shared/model/parser';
import {Loader} from '@/shared/ui/loader/loader';
import {PageLayout} from "@shared/ui/page-layout";
import {ParseResultDto} from "@shared/api";

import s from './result.module.css'
import {ParseUrlItem} from "@/pages/result/ui/parse-url-item";
import clsx from "clsx";
import {Button, JsonViewer} from "@shared/ui";
import {DownloadIcon} from "lucide-react";

type TabVariant = 'visual' | 'json'

export function ResultPage() {
  const {id} = useParams();
  const [result, setResult] = useState<ParseResultDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;

    const fetchResult = async () => {
      try {
        const data = await getResultById(id as string);
        setResult(data);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [id]);

  const [variant, setVariant] = useState<TabVariant>('visual')

  const onChangeTab = (variant: TabVariant) => {
    document.documentElement.scrollTo({
      top: 0,
      behavior: 'smooth',
    })

    setVariant(variant)
  }

  const onClickDownload = (type: 'json' | 'xml' | 'yaml') => {
    if (!result) return;

    if (type === 'json') {
      window.open(`http://localhost:3000/parser/${result?._id}/downloadJson`, '_blank');
      return;
    }

    if (type === 'xml') {
      window.open(`http://localhost:3000/parser/${result?._id}/downloadXml`, '_blank');
      return;
    }

    if (type === 'yaml') {
      window.open(`http://localhost:3000/parser/${result?._id}/downloadYaml`, '_blank');
      return;
    }
  }

  if (loading) return <Loader label='Получение данных...'/>;
  if (error) return <div>Error: {error}</div>;
  if (!result) return <div>No result found</div>;

  return (
    <PageLayout>
      <div className={s.header}>
        <div>
          <h1>Результат парсинга</h1>
          <p>ID: {result._id}, CNT: {result.results.length}</p>
        </div>

        <div className={s.downloadWrapper}>
          <Button className={s.downloadButton}>
            <DownloadIcon/>
            Скачать данные
            <div className={s.dropdownWrapper}>
              <div className={s.dropdownMenu}>
                <div onClick={() => onClickDownload('json')} className={s.dropdownItem}>Скачать в JSON</div>
                <div onClick={() => onClickDownload('xml')} className={s.dropdownItem}>Скачать в XML</div>
                <div onClick={() => onClickDownload('yaml')} className={s.dropdownItem}>Скачать в YAML</div>
              </div>
            </div>
          </Button>
        </div>
      </div>

      <div className={s.tabs}>
        <div onClick={() => onChangeTab('visual')} className={clsx(s.tab, variant === 'visual' && s.active)}>Визуально
        </div>
        <div onClick={() => onChangeTab('json')} className={clsx(s.tab, variant === 'json' && s.active)}>JSON</div>
      </div>

      {variant === 'visual' && <div className={s.container}>
        {result.results.map(result => (
          <ParseUrlItem key={result.url} item={result}/>
        ))}
      </div>}

      {variant === 'json' && (
        <div className={s.json}>
          <JsonViewer data={result.results}/>
        </div>
      )}
    </PageLayout>
  );
}
