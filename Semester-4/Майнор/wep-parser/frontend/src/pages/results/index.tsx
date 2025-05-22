import { useUnit, useGate } from 'effector-react';
import { $results, $isLoading, $parsingError, ResultsGate } from '../../shared/model/parser';
import { Loader } from '../../shared/ui/loader/loader';
import { Header } from '../../widgets/header';

export const ResultsPage = () => {
  const { results, isLoading, error } = useUnit({
    results: $results,
    isLoading: $isLoading,
    error: $parsingError
  });

  if (isLoading) {
    return <Loader />;
  }

  if (error) {
    return (
      <div>
        <h1>Ошибка парсинга</h1>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Результаты парсинга</h1>
      <pre>{JSON.stringify(results, null, 2)}</pre>
    </div>
  );
};
