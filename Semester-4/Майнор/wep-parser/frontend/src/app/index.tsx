import { Header } from '@widgets/header';
import { UrlInputList } from '@features/url-input-list';
import styles from './app.module.css';

export const App = () => {
  return (
    <div className={styles.app}>
      <Header />
      <main className={styles.main}>
        <UrlInputList />
      </main>
    </div>
  );
};
