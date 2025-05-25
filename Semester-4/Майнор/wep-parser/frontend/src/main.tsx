import {createRoot} from 'react-dom/client';
import {App} from './app';
import './app/styles/global.css';
import './app/styles/normalize.css';

createRoot(document.getElementById('root')!).render(
  <App/>
);
