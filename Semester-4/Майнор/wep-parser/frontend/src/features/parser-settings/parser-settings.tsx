import { useUnit } from 'effector-react';
import { $parserSettings, updateParserSettings } from '../../shared/model/parser';
import { Settings } from 'lucide-react';
import { Button } from '../../shared/ui/button';
import styles from './parser-settings.module.css';

export const ParserSettings = () => {
  const settings = useUnit($parserSettings);
  const updateSettings = useUnit(updateParserSettings);

  return (
    <div className={styles.settingsContainer}>
      <Button variant="icon" aria-label="Настройки парсера">
        <Settings size={20} />
      </Button>
      
      <div className={styles.settingsPanel}>
        <div className={styles.settingsGroup}>
          <label>Глубина вложенности:</label>
          <div className={styles.numberInput}>
            <button 
              onClick={() => updateSettings({ depth: Math.max(1, settings.depth - 1) })}
              disabled={settings.depth <= 0}
            >
              -
            </button>
            <input 
              type="number" 
              min="0" 
              max="5"
              value={settings.depth}
              onChange={(e) => {
                const value = parseInt(e.target.value);
                if (!isNaN(value) && value >= 0 && value <= 5) {
                  updateSettings({ depth: value });
                }
              }}
            />
            <button 
              onClick={() => updateSettings({ depth: Math.min(5, settings.depth + 1) })}
              disabled={settings.depth >= 5}
            >
              +
            </button>
          </div>
        </div>

        <div className={styles.settingsGroup}>
          <label>
            <input
              type="checkbox"
              checked={settings.extractLinks}
              onChange={(e) => updateSettings({ extractLinks: e.target.checked })}
            />
            Собирать ссылки
          </label>

          <label>
            <input
              type="checkbox"
              checked={settings.extractTitles}
              onChange={(e) => updateSettings({ extractTitles: e.target.checked })}
            />
            Собирать заголовки
          </label>

          <label>
            <input
              type="checkbox"
              checked={settings.extractImages}
              onChange={(e) => updateSettings({ extractImages: e.target.checked })}
            />
            Собирать изображения
          </label>

          <label>
            <input
              type="checkbox"
              checked={settings.extractDescriptions}
              onChange={(e) => updateSettings({ extractDescriptions: e.target.checked })}
            />
            Собирать описания
          </label>

          <label>
            <input
              type="checkbox"
              checked={settings.extractTextContent}
              onChange={(e) => updateSettings({ extractTextContent: e.target.checked })}
            />
            Собирать текстовый контент
          </label>
        </div>
      </div>
    </div>
  );
};
