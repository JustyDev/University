import s from './header.module.css';
import {Link} from 'react-router-dom';

export const Header = () => {
  return (
    <header className={s.header}>
      <div className={s.container}>
        <h1 className={s.title}>Dynamic Web Parser</h1>
        <nav className={s.nav}>
          <Link to="/" className={s.link}>Главная</Link>
          <Link to="/history" className={s.link}>История парсинга</Link>
        </nav>
      </div>
    </header>
  );
};
