
def add_to_first(tape):
    """Сложение двух чисел с записью результата на месте первого числа."""
    i = 0
    # Пропустим первое число
    while tape[i] == 'X':
        i += 1
    # Пропустим пробел
    i += 1
    # Начнем переносить символы X из второго числа в первое
    while tape[i] == 'X':
        tape[i] = ' '
        k = 0
        while tape[k] == 'X':
            k += 1
        tape[k] = 'X'
        i += 1
    return tape

def add_to_second(tape):
    """Сложение двух чисел с записью результата на месте второго числа."""
    i = 0
    # Пропустим первое число
    while tape[i] == 'X':
        i += 1
    # Пропустим пробел
    i += 1
    # Найдем конец второго числа
    end = i
    while tape[end] == 'X':
        end += 1
    # Начнем переносить X из первого числа в конец второго
    k = 0
    while tape[k] == 'X':
        k += 1
    while k > 0:
        end -= 1
        tape[end] = 'X'
        k -= 1
    return tape

def subtract(tape):
    """Вычитание второго числа из первого с записью результата на месте первого числа."""
    i = 0
    # Пропустим первое число
    while tape[i] == 'X':
        i += 1
    # Пропустим пробел
    i += 1
    # Начнем вычитание
    while tape[i] == 'X':
        j = 0
        # Найдем первый X в первом числе
        while tape[j] != 'X':
            j += 1
        # Удалим X из первого числа
        tape[j] = ' '
        # Удалим X из второго числа
        tape[i] = ' '
        i += 1
    return tape

def main():
    print("Сложение с записью на первое число:")
    tape = list("XXXX XXXXXX")
    result = add_to_first(tape)
    print(''.join(result))

    print("Сложение с записью на второе число:")
    tape = list("XXXX XXXXXX")
    result = add_to_second(tape)
    print(''.join(result))

    print("Вычитание второго из первого:")
    tape = list("XXXXXX XXXX")
    result = subtract(tape)
    print(''.join(result))

if __name__ == "__main__":
    main()
