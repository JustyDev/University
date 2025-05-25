import {PlusCircle, Trash2} from 'lucide-react';
import clsx from 'clsx';
import {Button, Input} from '../../shared/ui';
import s from './url-input-list.module.css';
import {ChangeEvent, ReactNode} from 'react';
import {ParserSettings} from "@features/parser-settings/parser-settings.tsx";

interface UrlInputItemProps {
  id: string;
  value: string;
  isLast: boolean;
  count: number;
  onChange: (id: string, value: string) => void;
  onAdd: () => void;
  onRemove?: (id: string) => void;
  additional?: ReactNode;
}

export const UrlInputItem = ({id, value, isLast, count, onChange, onAdd, onRemove, additional}: UrlInputItemProps) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(id, e.target.value);
  };

  return (
    <div className={s.inputRow}>
      <Input
        placeholder="Введите ссылку на сайт..."
        value={value}
        onChange={handleChange}
        className={s.urlInput}
      />
      {isLast ? (
        <Button
          variant="icon"
          onClick={onAdd}
          aria-label="Добавить URL"
          title="Добавить URL"
          disabled={count >= 5}
        >
          <PlusCircle size={20}/>
        </Button>
      ) : (
        <Button
          variant="icon"
          onClick={() => onRemove?.(id)}
          aria-label="Удалить URL"
          title="Удалить URL"
          className={clsx(s.deleteButton, {
            [s.hidden]: isLast
          })}
        >
          <Trash2 size={20}/>
        </Button>
      )}
      {isLast && (
        <ParserSettings/>
      )}
      {additional}
    </div>
  );
};
