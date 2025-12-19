#include <iostream>
#include <fstream>

// Макросы
#define MAIN_FUNCTION int main()
#define BEGIN {
#define END }
#define DO_DO do
#define WHILE_WHILE(cond) while(cond)
#define OPEN_FILE_IN(file, name) std::ifstream file(name)
#define OPEN_FILE_OUT(file, name) std::ofstream file(name)
#define CLOSE_FILE(file) file.close()
#define READ_DOUBLE(file, var) file >> var
#define WRITE_DOUBLE(file, var) file << var << std::endl

MAIN_FUNCTION BEGIN
    double x;
    // Открыть файл для записи
    OPEN_FILE_OUT(fout, "number.txt");
    std::cout << "Введите вещественное число: ";
    std::cin >> x;

    // Записать число в файл
    WRITE_DOUBLE(fout, x);
    CLOSE_FILE(fout);

    // Открыть файл для чтения
    OPEN_FILE_IN(fin, "number.txt");
    double y;

    // Прочитать из файла с помощью do-while (как пример!)
    int count = 0;
    DO_DO BEGIN
        READ_DOUBLE(fin, y);
        std::cout << "Прочитано число из файла: " << y << std::endl;
        count++;
    END WHILE_WHILE(count < 1);

    CLOSE_FILE(fin);

    return 0;
END
