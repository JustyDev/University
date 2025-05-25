import {useUnit} from 'effector-react';
import {$parserSettings, updateParserSettings} from '../../shared/model/parser';
import {Settings} from 'lucide-react';
import {Button} from '../../shared/ui/button';
import {Checkbox} from '../../shared/ui/checkbox';
import s from './parser-settings.module.css';

export const ParserSettings = () => {
  const settings = useUnit($parserSettings);
  const updateSettings = useUnit(updateParserSettings);

  return (
    <div className={s.settingsContainer}>
      <Button variant="icon" aria-label="Настройки парсера">
        <Settings size={20}/>
      </Button>

      <div className={s.tooltipWrapper}>
        <div className={s.settingsPanel}>
          <div className={s.settingsGroup}>
            <div className={s.checkboxGroupTitle}>Глубина вложенности:</div>
            <div className={s.depthControl}>
              <div className={s.depthInput}>
                <input
                  type="number"
                  min="1"
                  max="5"
                  value={settings.depth}
                  onChange={(e) => {
                    const value = parseInt(e.target.value);
                    if (!isNaN(value) && value >= 1 && value <= 5) {
                      updateSettings({depth: value});
                    }
                  }}
                />
              </div>
              <div className={s.depthButtons}>
                <button
                  onClick={() => updateSettings({depth: Math.max(1, settings.depth - 1)})}
                  disabled={settings.depth <= 1}
                >
                  -
                </button>
                <button
                  onClick={() => updateSettings({depth: Math.min(5, settings.depth + 1)})}
                  disabled={settings.depth >= 5}
                >
                  +
                </button>
              </div>
            </div>
          </div>

          <div className={s.checkboxGroup}>
            <div className={s.checkboxGroupTitle}>Анализировать ссылки:</div>
            <div className={s.checkboxGrid}>
              <Checkbox
                label="Внутренние"
                checked={settings.extractInternalLinks}
                onChange={(e) => updateSettings({extractInternalLinks: e.target.checked})}
              />
              <Checkbox
                label="Внешние"
                checked={settings.extractExternalLinks}
                onChange={(e) => updateSettings({extractExternalLinks: e.target.checked})}
              />
            </div>
          </div>

          <div className={s.checkboxGroup}>
            <div className={s.checkboxGroupTitle}>Анализировать заголовки:</div>
            <div className={s.checkboxGrid}>
              {[1, 2, 3, 4, 5, 6].map((level) => (
                <Checkbox
                  key={`h${level}`}
                  label={`H${level}`}
                  checked={settings[`extractH${level}` as keyof typeof settings] as boolean}
                  onChange={(e) => updateSettings({[`extractH${level}`]: e.target.checked})}
                />
              ))}
            </div>
          </div>

          <div className={s.checkboxGroup}>
            <div className={s.checkboxGroupTitle}>Дополнительно:</div>
            <div className={s.checkboxColumn}>
              <Checkbox
                label="Анализировать описание"
                checked={settings.extractDescriptions}
                onChange={(e) => updateSettings({extractDescriptions: e.target.checked})}
              />
              <Checkbox
                label="Анализировать изображения"
                checked={settings.extractImages}
                onChange={(e) => updateSettings({extractImages: e.target.checked})}
              />
              <Checkbox
                label="Анализировать текстовый контент"
                checked={settings.extractTextContent}
                onChange={(e) => updateSettings({extractTextContent: e.target.checked})}
              />
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};
