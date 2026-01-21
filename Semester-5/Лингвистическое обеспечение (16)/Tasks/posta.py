
def add_to_first(tape):
    """Сложение двух чисел с записью результата на месте первого числа."""
    i = 0
    while tape[i] == 'X':
        i += 1
    i += 1
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
    while tape[i] == 'X':
        i += 1
    i += 1
    end = i
    while tape[end] == 'X':
        end += 1
    k = 0
    while tape[k] == 'X':
        k += 1
    while k > 0:
        end -= 1
        tape[end] = 'X'
        k -= 1
    return tape

def subtract_from_first(tape):
    """Вычитание второго числа из первого с записью результата на месте первого числа."""
    i = 0
    while tape[i] == 'X':
        i += 1
    i += 1
    while tape[i] == 'X':
        j = 0
        while tape[j] != 'X':
            j += 1
        tape[j] = ' '
        tape[i] = ' '
        i += 1
    return tape

def subtract_from_second(tape):
    """Вычитание первого числа из второго с записью результата на месте второго числа."""
    i = 0
    while tape[i] == 'X':
        i += 1
    i += 1
    while tape[i] != ' ':
        i += 1
    i += 1
    while tape[i] == 'X':
        j = 0
        while tape[j] != 'X':
            j += 1
        tape[j] = ' '
        tape[i] = ' '
        i += 1
    return tape

def shift_right(tape):
    """Сдвиг числа вправо через пробел."""
    i = 0
    while tape[i] == 'X':
        i += 1
    tape[i] = ' '
    i += 1
    while tape[i] == ' ':
        i += 1
    tape[i - 1] = 'X'
    return tape

def copy_right(tape):
    """Копирование числа вправо через пробел."""
    i = 0
    while tape[i] == 'X':
        i += 1
    i += 1
    end = i
    while end < len(tape) and tape[end] == ' ':
        end += 1
    while i < end and tape[i - 1] == ' ':
        if tape[i] == 'X':
            tape[end] = 'X'
            end += 1
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
    result = subtract_from_first(tape)
    print(''.join(result))

    print("Вычитание первого из второго:")
    tape = list("XXXX XXXXXX")
    result = subtract_from_second(tape)
    print(''.join(result))

    print("Сдвиг числа вправо через пробел:")
    tape = list("XXXX ")
    result = shift_right(tape)
    print(''.join(result))

    print("Копирование числа вправо через пробел:")
    tape = list("XXXX ")
    result = copy_right(tape)
    print(''.join(result))

if __name__ == "__main__":
    main()
