import {useUnit} from 'effector-react';
import {Button} from '../../shared/ui';
import {
  $parserSettings,
  $urlInputs,
  addUrlInput,
  parseUrls,
  removeUrlInput,
  resetInputs,
  updateUrlInput
} from '../../shared/model/parser';
import {UrlInputItem} from './url-input-item';
import s from './url-input-list.module.css';

export const UrlInputList = () => {
  const {urlInputs, parserSettings} = useUnit({
    urlInputs: $urlInputs,
    parserSettings: $parserSettings
  });

  const onClickParse = () => {
    const urls = urlInputs.map(input => input.value).filter(Boolean);
    if (urls.length > 0) {
      const settings = parserSettings
      parseUrls({urls, settings});
      resetInputs();
    }
  };

  const handleChange = (id: string, value: string) => {
    updateUrlInput({id, value});
  };

  return (
    <div className={s.container}>
      {urlInputs.map((input, index) => (
        <UrlInputItem
          key={input.id}
          id={input.id}
          value={input.value}
          isLast={index === urlInputs.length - 1}
          count={urlInputs.length}
          onChange={handleChange}
          onAdd={addUrlInput}
          onRemove={removeUrlInput}
          additional={index === urlInputs.length - 1 && (
            <Button
              onClick={onClickParse}
              variant="primary"
              className={s.parseButton}
            >
              Парсить
            </Button>
          )}
        />
      ))}
    </div>
  );
};
