import os
import shutil
import time

#---------------------1------------------------------
def create_directory(path):
    try:
        os.makedirs(path)
        print(f"Директория {path} успешно создана.")
    except FileExistsError:
        print(f"Директория {path} уже существует!")
    except Exception as e:
        print(f"Ошибка при создании директории: {e}")

#---------------------2------------------------------
def delete_directory(path):
    if not os.path.exists(path):
        print(f"Директория {path} не найдена!")
        return

    if os.listdir(path):
        print(f"Директория {path} не пуста!")
        confirm = input("Уверены, что хотите удалить папку?(y/n): ").lower()
        if confirm != 'y':
            print("Отмена удаления.")
            return
    try:
        shutil.rmtree(path)
        print(f"Директория {path} удалена.")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")

#---------------------3------------------------------
def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
        print(f"Файл скопирован из '{src}' в '{dst}'")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")

#---------------------4------------------------------
def move_or_rename_file(src, dst):
    try:
        shutil.move(src, dst)
        print(f"Файл перемещён или переименован в '{dst}'")
    except Exception as e:
        print(f"Ошибка при перемещении/переименовании: {e}")

#---------------------5------------------------------
def delete_file(path):
    try:
        os.remove(path)
        print(f"Файл '{path}' удалён.")
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")

#---------------------6------------------------------
def check_existence(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            print(f"'{path}' — директория.")
        elif os.path.isfile(path):
            print(f"'{path}' — файл.")
        else:
            print(f"'{path}' существует, но это не файл и не директория.")
    else:
        print(f"'{path}' не существует.")

#---------------------7------------------------------
def list_directory(path):
    if not os.path.isdir(path):
        print(f"Путь '{path}' не является директорией.")
        return
    print(f"Содержимое директории '{path}':")
    try:
        for item in os.listdir(path):
            print("•", item)
    except Exception as e:
        print(f"Ошибка при чтении директории: {e}")

#---------------------8------------------------------
def file_info(path):
    if not os.path.isfile(path):
        print(f"'{path}' не является файлом.")
        return
    try:
        size = os.path.getsize(path)
        modified_time = os.path.getmtime(path)
        print(f"Информация о файле '{path}':")
        print(f"Размер: {size} байт")
        print(f"Последнее изменение: {time.ctime(modified_time)}")
    except Exception as e:
        print(f"Ошибка при получении информации: {e}")

#---------------------------------------------------
def main():
    actions_with_path = {
        1: create_directory,
        2: delete_directory,
        5: delete_file,
        6: check_existence,
        7: list_directory,
        8: file_info
    }
    while True:
        print("""
    Выберите действие:
    1 — Создать директорию
    2 — Удалить директорию
    3 — Копировать файл
    4 — Переместить/переименовать файл
    5 — Удалить файл
    6 — Проверить существование файла/директории
    7 — Показать содержимое директории
    8 — Получить информацию о файле
    0 — Выход
    """)

        try:
            choice = int(input("Ваш выбор: "))
        except ValueError:
            print("Ошибка: введите номер действия (0-8).")
            continue

        if choice in actions_with_path:
            path = input("Введите путь: ").strip()
            actions_with_path[choice](path)
            continue

        match choice:
            case 3:
                src = input("Путь к исходному файлу: ").strip()
                dst = input("Путь назначения: ").strip()
                copy_file(src, dst)
            case 4:
                src = input("Путь к исходному файлу: ").strip()
                dst = input("Новый путь или новое имя: ").strip()
                move_or_rename_file(src, dst)
            case 0:
                print("Выход из программы.")
                break
            case _:
                print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()