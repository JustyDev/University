import { useUnit } from 'effector-react';
import { $urlInputs, $parserSettings, addUrlInput, updateUrlInput, removeUrlInput, parseUrls } from '../../shared/model/parser';
import { ParserSettings } from '../parser-settings/parser-settings';
import { UrlInputItem } from './url-input-item';
import styles from './url-input-list.module.css';
import { useNavigate } from 'react-router-dom';

export const UrlInputList = () => {
  const { urlInputs, parserSettings } = useUnit({
    urlInputs: $urlInputs,
    parserSettings: $parserSettings
  });
  const navigate = useNavigate();
  const removeInput = useUnit(removeUrlInput);

  const parseUrlsEvent = useUnit(parseUrls);

  const onClickParse = () => {
    const urls = urlInputs.map(input => input.value).filter(Boolean);
    if (urls.length > 0) {
      const settings = parserSettings
      parseUrlsEvent({ urls, settings });
      navigate('/results');
    }
  };

  const handleChange = (id: string, value: string) => {
    updateUrlInput({ id, value });
  };

  const handleAdd = () => {
    addUrlInput();
  };

  return (
    <div className={styles.container}>
      <div className={styles.inputRow}>
        <div className={styles.settingsWrapper}>
          <ParserSettings />
        </div>
      </div>
      {urlInputs.map((input, index) => (
        <UrlInputItem
          key={input.id}
          id={input.id}
          value={input.value}
          isLast={index === urlInputs.length - 1}
          onChange={handleChange}
          onAdd={handleAdd}
          onParse={onClickParse}
          onRemove={removeInput}
        />
      ))}
    </div>
  );
};
