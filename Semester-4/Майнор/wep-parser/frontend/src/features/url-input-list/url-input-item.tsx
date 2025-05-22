import { PlusCircle, X } from 'lucide-react';
import clsx from 'clsx';
import { Button, Input } from '../../shared/ui';
import styles from './url-input-list.module.css';
import { ChangeEvent } from 'react';

interface UrlInputItemProps {
  id: string;
  value: string;
  isLast: boolean;
  onChange: (id: string, value: string) => void;
  onAdd: () => void;
  onParse: () => void;
  onRemove?: (id: string) => void;
}

export const UrlInputItem = ({ id, value, isLast, onChange, onAdd, onParse, onRemove }: UrlInputItemProps) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(id, e.target.value);
  };

  return (
    <div className={styles.inputRow}>
      <Input
        placeholder="Введите URL"
        value={value}
        onChange={handleChange}
        className={styles.urlInput}
      />
      {isLast ? (
        <Button
          variant="icon"
          onClick={onAdd}
          aria-label="Добавить URL"
          title="Добавить URL"
        >
          <PlusCircle size={20} />
        </Button>
      ) : (
        <Button
          variant="icon"
          onClick={() => onRemove?.(id)}
          aria-label="Удалить URL"
          title="Удалить URL"
          className={clsx(styles.deleteButton, {
            [styles.hidden]: isLast
          })}
        >
          <X size={20} />
        </Button>
      )}
      {isLast && (
        <Button
          onClick={onParse}
          variant="primary"
          className={styles.parseButton}
        >
          Парсить
        </Button>
      )}
    </div>
  );
};
