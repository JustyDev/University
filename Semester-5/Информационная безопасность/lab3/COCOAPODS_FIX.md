# Исправление проблемы с CocoaPods

## Проблема
При запуске `flutter run` появляется ошибка:
```
Warning: CocoaPods not installed. Skipping pod install.
```

## Решение

CocoaPods установлен, но не находится в PATH. Добавьте его в PATH:

### Временное решение (для текущей сессии терминала)
```bash
export PATH="/opt/homebrew/lib/ruby/gems/3.4.0/bin:$PATH"
flutter run -d ios
```

### Постоянное решение

Добавьте путь к CocoaPods в ваш shell конфигурационный файл:

**Для zsh (по умолчанию на macOS):**
```bash
echo 'export PATH="/opt/homebrew/lib/ruby/gems/3.4.0/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Для bash:**
```bash
echo 'export PATH="/opt/homebrew/lib/ruby/gems/3.4.0/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

### Проверка
После добавления в PATH проверьте:
```bash
which pod
# Должно вывести: /opt/homebrew/lib/ruby/gems/3.4.0/bin/pod
```

## Альтернативное решение

Если предыдущее не помогло, можно создать симлинк:
```bash
sudo ln -s /opt/homebrew/lib/ruby/gems/3.4.0/bin/pod /usr/local/bin/pod
```

## После исправления

Теперь вы можете запускать приложение обычной командой:
```bash
flutter run -d ios
```

или

```bash
flutter run -d <device-id>
