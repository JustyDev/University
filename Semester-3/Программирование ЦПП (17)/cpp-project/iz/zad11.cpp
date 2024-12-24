#include <iostream>
#include <cstring>

int main() {
    const int k = 100;
    char array[k + 2];

    std::cout << "Введите массив символов, за которым следует точка: ";
    std::cin.getline(array, k + 2);

    int length = std::strlen(array);
    if (array[length - 1] != '.') {
        std::cout << "Ошибка: строка должна заканчиваться точкой." << std::endl;
        return 1;
    }

    std::cout << "Текст в обратном порядке: ";
    for (int i = length - 2; i >= 0; --i) {
        std::cout << array[i];
    }
    std::cout << "." << std::endl;

    return 0;
}