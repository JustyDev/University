import {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';
import {getResultById} from '@/shared/model/parser';
import {Loader} from '@/shared/ui/loader/loader';
import {PageLayout} from "@shared/ui/page-layout";
import {ParseResultDto} from "@shared/api";

import s from './result.module.css'
import {ParseUrlItem} from "@/pages/result/ui/parse-url-item";

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

  if (loading) return <Loader/>;
  if (error) return <div>Error: {error}</div>;
  if (!result) return <div>No result found</div>;

  return (
    <PageLayout>
      <h1>Результат парсинга</h1>
      <p>ID: {result._id}</p>

      <div className={s.container}>
        {result.results.map(result => (
          <ParseUrlItem key={result.url} item={result}/>
        ))}
      </div>
    </PageLayout>
  );
}
