import styles from './header.module.css';
import { Link } from 'react-router-dom';

export const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <h1 className={styles.title}>Web Parser</h1>
        <nav className={styles.nav}>
          <Link to="/" className={styles.link}>Главная</Link>
          <Link to="/common" className={styles.link}>Common</Link>
        </nav>
      </div>
    </header>
  );
};
