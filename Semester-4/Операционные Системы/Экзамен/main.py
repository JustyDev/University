import rumps
import os
import time
import threading
from pathlib import Path
import subprocess


class LogCleanerApp(rumps.App):
    def __init__(self):
        super(LogCleanerApp, self).__init__("🧹", "Log Cleaner")
        self.folder_to_clean = None
        self.cleaning_thread = None
        self.auto_clean_thread = None
        self.is_cleaning = False
        self.auto_clean_enabled = False
        self.auto_clean_interval = 60

        self.auto_clean_menu_item = rumps.MenuItem("Включить автоочистку (1 мин)")
        self.menu = [
            "Выбрать папку для очистки",
            "Очистить .log файлы сейчас",
            None,
            self.auto_clean_menu_item,
            "Показать текущую папку",
            None,
            "Выход"
        ]

        self.start_auto_clean_monitor()

    def start_auto_clean_monitor(self):
        self.auto_clean_thread = threading.Thread(target=self._auto_clean_monitor, daemon=True)
        self.auto_clean_thread.start()

    def _auto_clean_monitor(self):
        while True:
            if self.auto_clean_enabled and self.folder_to_clean and not self.is_cleaning:
                self.is_cleaning = True
                self._clean_logs(auto_mode=True)
                self.is_cleaning = False

            time.sleep(self.auto_clean_interval)

    @rumps.clicked("Выбрать папку для очистки")
    def select_folder(self, _):
        applescript = '''
        tell application "System Events"
            activate
            set folderPath to POSIX path of (choose folder with prompt "Выберите папку для очистки .log файлов")
        end tell
        '''

        try:
            result = subprocess.run(['osascript', '-e', applescript],
                                    capture_output=True, text=True, check=True)

            folder_path = result.stdout.strip()

            if folder_path:
                self.folder_to_clean = folder_path
                rumps.notification(
                    title="Log Cleaner",
                    subtitle="Папка выбрана",
                    message=f"Будет очищаться: {self.folder_to_clean}"
                )
        except subprocess.CalledProcessError:
            pass
        except Exception as e:
            rumps.notification(
                title="Log Cleaner",
                subtitle="Ошибка",
                message=f"Не удалось выбрать папку: {str(e)}"
            )

    @rumps.clicked("Очистить .log файлы сейчас")
    def clean_logs_now(self, _):
        if not self.folder_to_clean:
            rumps.notification(
                title="Log Cleaner",
                subtitle="Ошибка",
                message="Сначала выберите папку для очистки"
            )
            return

        if self.is_cleaning:
            rumps.notification(
                title="Log Cleaner",
                subtitle="Уже выполняется",
                message="Очистка уже выполняется"
            )
            return

        self.is_cleaning = True
        self.cleaning_thread = threading.Thread(target=lambda: self._clean_logs(auto_mode=False))
        self.cleaning_thread.start()

    def _clean_logs(self, auto_mode=False):
        try:
            log_files = list(Path(self.folder_to_clean).glob("**/*.log"))
            count = len(log_files)

            if count == 0:
                rumps.notification(
                    title="Log Cleaner",
                    subtitle="Информация",
                    message="Файлы .log не найдены"
                )
            else:
                for log_file in log_files:
                    os.remove(log_file)

                rumps.notification(
                    title="Log Cleaner",
                    subtitle="Успешно",
                    message=f"Удалено {count} .log файлов"
                )
        except Exception as e:
            if not auto_mode:
                rumps.notification(
                    title="Log Cleaner",
                    subtitle="Ошибка",
                    message=f"Ошибка при очистке: {str(e)}"
                )
        finally:
            if not auto_mode:
                self.is_cleaning = False

    @rumps.clicked("Включить автоочистку (1 мин)")
    def toggle_auto_clean(self, sender):
        self.auto_clean_enabled = not self.auto_clean_enabled

        if self.auto_clean_enabled:
            sender.title = "Выключить автоочистку"
            # Проверяем, выбрана ли папка
            if not self.folder_to_clean:
                rumps.notification(
                    title="Log Cleaner",
                    subtitle="Внимание",
                    message="Папка для очистки не выбрана. Автоочистка не будет работать."
                )
            else:
                rumps.notification(
                    title="Log Cleaner",
                    subtitle="Автоочистка включена",
                    message=f"Автоматическая очистка папки каждую минуту включена"
                )
        else:
            sender.title = "Включить автоочистку (1 мин)"
            rumps.notification(
                title="Log Cleaner",
                subtitle="Автоочистка выключена",
                message="Автоматическая очистка отключена"
            )

    @rumps.clicked("Показать текущую папку")
    def show_current_folder(self, _):
        auto_status = "включена" if self.auto_clean_enabled else "выключена"

        if self.folder_to_clean:
            rumps.notification(
                title="Log Cleaner",
                subtitle=f"Автоочистка {auto_status}",
                message=f"Текущая папка: {self.folder_to_clean}"
            )
        else:
            rumps.notification(
                title="Log Cleaner",
                subtitle=f"Автоочистка {auto_status}",
                message="Папка для очистки не выбрана"
            )

    @rumps.clicked("Выход")
    def quit_app(self, _):
        rumps.quit_application()


if __name__ == "__main__":
    LogCleanerApp().run()
