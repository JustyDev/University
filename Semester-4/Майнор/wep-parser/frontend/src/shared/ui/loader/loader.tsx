import s from './loader.module.css';

type LoaderProps = {
  label?: string
}

export const Loader = ({label}: LoaderProps) => (
  <div className={s.loader}>
    <div className={s.spinner}></div>
    <p>{label ? label : 'Парсинг данных...'}</p>
  </div>
);
