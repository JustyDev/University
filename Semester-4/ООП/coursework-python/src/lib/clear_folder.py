import os
import shutil


def clear_folder(folder_path):
    """
    Очищает указанную папку от всех файлов.
    Если папки не существует, создает её.

    Args:
        folder_path (str): Путь к папке, которую нужно очистить
    """
    # Проверяем существует ли папка
    if os.path.exists(folder_path):
        # Если папка существует, удаляем все её содержимое
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # удаляем файл или символическую ссылку
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # удаляем подпапку со всем содержимым
            except Exception as e:
                print(f'Ошибка при удалении папки {file_path}. Причина: {e}')
    else:
        # Если папки нет, создаем её
        os.makedirs(folder_path)