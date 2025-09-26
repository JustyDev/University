// ЛР №3. Макросы с параметрами.
// Вариант 16: main, do-while, открытие/закрытие файла, запись и чтение вещественного числа.

#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>

// Описание главной функции
#define MAIN           int main

// Оператор цикла do-while
#define DO             do
#define WHILE(cond)    while (cond)

// Открытие/закрытие файла и операции с вещественными
#define OPEN_OUT(ofs, path)   std::ofstream ofs(path)
#define OPEN_IN(ifs, path)    std::ifstream ifs(path)
#define WRITE_REAL(stream, x) (stream) << std::fixed << std::setprecision(6) << (x) << '\n'
#define READ_REAL(stream, x)  (stream) >> (x)
#define CLOSE(stream)         (stream).close()

MAIN() {
    // Запись трёх вещественных чисел в файл с помощью do-while
    OPEN_OUT(outf, "nums.txt");
    if (!outf) {
        std::cerr << "Не удалось открыть файл на запись\n";
        return 1;
    }

    double base = 1.1;
    int count = 0;

    DO {
        WRITE_REAL(outf, base + count); // 1.1, 2.1, 3.1
        ++count;
    } WHILE (count < 3);

    CLOSE(outf);

    // Чтение из файла и суммирование
    OPEN_IN(inf, "nums.txt");
    if (!inf) {
        std::cerr << "Не удалось открыть файл на чтение\n";
        return 1;
    }

    double x = 0.0, sum = 0.0;
    while (READ_REAL(inf, x)) { // читаем пока успешно
        sum += x;
    }
    CLOSE(inf);

    std::cout << "Сумма прочитанных чисел: " << std::fixed << std::setprecision(6) << sum << std::endl;
    return 0;
}
