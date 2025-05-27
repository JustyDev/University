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
import {useState} from "react";
import {isValidUrl} from "@shared/lib/is-valid-url.ts";

export const UrlInputList = () => {
  const {urlInputs, parserSettings} = useUnit({
    urlInputs: $urlInputs,
    parserSettings: $parserSettings
  });

  const [errors, setErrors] = useState<{ idx: number, text: string }[]>([]);

  const onClickParse = () => {
    const urls = urlInputs.map(input => input.value).filter(Boolean);

    let hasErrors = false

    urls.map((url, idx) => {
      if (!isValidUrl(url)) {
        hasErrors = true
        setErrors(errors => [
          ...errors,
          {
            idx,
            text: url,
          }
        ])
      }
    })

    if (hasErrors) return;

    if (urls.length > 0) {
      const settings = parserSettings
      parseUrls({urls, settings});
      resetInputs();
    }
  };

  const handleChange = (id: string, value: string) => {
    updateUrlInput({id, value});
    setErrors([])
  };

  return (
    <div className={s.container}>
      {urlInputs.map((input, index) => (
        <UrlInputItem
          key={input.id}
          id={input.id}
          value={input.value}
          error={errors?.find(arr => arr.idx === index)?.text}
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
