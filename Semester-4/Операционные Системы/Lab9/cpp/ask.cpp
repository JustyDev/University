#include <iostream>
#include <cctype>
using std::cout, std::cin;

int main() {
    std::cout << "[c] Запустить компиляцию\n";
    std::cout << "[e] Редактировать программу на C++\n";
    std::cout << "[x] Выйти\n";
    std::cout << "Ваш выбор: ";

    char choice;
    std::cin >> choice;

    switch (tolower(choice)) {
        case 'c':
            return 1; // Компиляция
        case 'e':
            return 2; // Редактирование
        case 'x':
            return 3; // Выход
        default:
            return 0; // Неверный выбор
    }
}
