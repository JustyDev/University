import styles from './loader.module.css';

export const Loader = () => (
  <div className={styles.loader}>
    <div className={styles.spinner}></div>
    <p>Парсинг данных...</p>
  </div>
);
