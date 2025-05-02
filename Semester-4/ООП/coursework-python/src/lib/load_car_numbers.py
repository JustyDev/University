def load_car_numbers(filename):
    db_numbers = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Удаляем пробелы и символы переноса строки
                car_number = line.strip()
                if car_number:  # Добавляем только непустые строки
                    db_numbers.append(car_number)
        print(f"Загружено {len(db_numbers)} номеров из файла {filename}")
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Используется пустая база номеров.")
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")

    return db_numbers