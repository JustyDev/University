def subtract_from_second(tape):
    """Вычитание первого числа из второго с записью результата на месте второго числа."""
    i = 0
    # Пропуск первого числа
    while tape[i] == 'X':
        i += 1
    # Пропуск пробела
    i += 1
    start_second = i
    # Перемещение к концу второго числа
    while i < len(tape) and tape[i] == 'X':
        i += 1
    # Удаление 'X' из первого числа
    j = 0
    while j < start_second - 1 and tape[j] == 'X':
        while tape[start_second] != 'X':
            start_second += 1
        tape[start_second] = ' '
        j += 1
    return tape


def shift_right(tape):
    """Сдвиг числа вправо через пробел."""
    # Найти конец первого числа
    i = 0
    while tape[i] == 'X':
        i += 1
    # Удаляем первый 'X'
    tape[i - 1] = ' '
    # Найти пробел справа
    while tape[i] == ' ':
        i += 1
    # Поставить 'X' после пробела
    tape[i - 1] = 'X'
    return tape


def copy_right(tape):
    """Копирование числа вправо через пробел."""
    i = 0
    # Найти конец первого числа
    while tape[i] == 'X':
        i += 1
    i += 1  # Перейти на пробел

    # Скопировать число в конец
    j = 0
    while j < i - 1 and tape[j] == 'X':
        while tape[i] == ' ':
            if j < len(tape):
                tape[i] = 'X'
                j += 1
            i += 1
    return tape


def main():
    print("Вычитание первого из второго:")
    tape = list("XXXX XXXXXX")
    result = subtract_from_second(tape)
    print(''.join(result))

    print("Сдвиг числа вправо через пробел:")
    tape = list("XXXX ")
    result = shift_right(tape)
    print(''.join(result))

    print("Копирование числа вправо через пробел:")
    tape = list("XXXX   ")
    result = copy_right(tape)
    print(''.join(result))


if __name__ == "__main__":
    main()
