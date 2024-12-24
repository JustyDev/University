#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>

struct Train {
    int number;            // Номер поезда
    char route[30];             // Пункт отправления-прибытия
    int ticketsSold;            // Количество проданных билетов
    float ticketPrice;          // Цена одного билета
};


void addRecord(const std::string& filename) {
    Train train;

    std::cout << "номер поезда: ";
    std::cin >> train.number;
    std::cin.ignore();

    std::cout << "пункт отправления-прибытия: ";
    std::cin.getline(train.route, sizeof(train.route));

    std::cout << "количество проданных билетов: ";
    std::cin >> train.ticketsSold;

    std::cout << "Цена билета: ";
    std::cin >> train.ticketPrice;

    std::ofstream file(filename, std::ios::binary | std::ios::app);
    if (!file.is_open()) {
        std::cout << "no such file" << std::endl;
        return;
    }

    file.write(reinterpret_cast<const char*>(&train), sizeof(Train));
    file.close();

    std::cout << "Запись добавлена." << std::endl;
}


void showAllRecords(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cout << "no such file" << std::endl;
        return;
    }

    Train train;
    std::cout << std::fixed << std::setprecision(2) << "Список поездов:\n";
    while (file.read(reinterpret_cast<char*>(&train), sizeof(Train))) {
        std::cout << "Номер поезда: " << train.number << std::endl;
        std::cout << "Пункт отправления-прибытия: " << train.route << std::endl;
        std::cout << "Количество проданных билетов: " << train.ticketsSold << std::endl;
        std::cout << "Цена одного билета: " << train.ticketPrice << std::endl;
        std::cout << "-----------------------------" << std::endl;
    }
    file.close();
}

void showEarnings(const std::string& filename) {
    int number;
    std::cout << "номер поезда для подсчёта выручки: ";
    std::cin >> number;

    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cout << "no such file" << std::endl;
        return;
    }

    Train train;
    bool found = false;
    float earn = 0.0;
    while (file.read(reinterpret_cast<char*>(&train), sizeof(Train)))
        if (train.number == number) {
            earn += train.ticketsSold * train.ticketPrice;
            found = true;
        }
    file.close();

    if (found)
        std::cout << "Общая выручка для поезда " << number << ": " << earn << std::endl;
    else std::cout << "Поезд с номером " << number << " не найден." << std::endl;
}

int menu() {
    std::cout << "\n===================RailwayBase=====================\n";
    std::cout << "1 - добавить запись;  2 - показать все запеиси;\n";
    std::cout << "3 - показать выручку поезда;  4 - выход;\n";
    std::cout << "===================================================\n";
    std::cout << "Ваш выбор: ";

    int choice;
    std::cin >> choice;
    return choice;
}

int main() {
    const std::string filename = "/Users/justy-dev/Documents/GitHub/University/Semester-3/Программирование ЦПП (17)/cpp-project/assets/railwaybase.dat";

    while (true) {
        int choice = menu();
        switch (choice) {
            case 1: addRecord(filename); break;
            case 2: showAllRecords(filename); break;
            case 3: showEarnings(filename); break;
            case 4: return 0;
            default: std::cout << "wrong choice" << std::endl;
        }
    }
}
