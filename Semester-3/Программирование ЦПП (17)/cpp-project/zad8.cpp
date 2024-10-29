#include <iostream>
#include <fstream>
#include <string>

void compareFiles(const std::string &file1, const std::string &file2) {
    std::ifstream inFile1(file1);
    std::ifstream inFile2(file2);

    if (!inFile1.is_open()) {
        std::cerr << "Ошибка открытия файла: " << file1 << std::endl;
        return;
    }

    if (!inFile2.is_open()) {
        std::cerr << "Ошибка открытия файла: " << file2 << std::endl;
        return;
    }

    std::string line1, line2;
    int lineNumber = 1;
    bool differencesFound = false;

    while (std::getline(inFile1, line1) && std::getline(inFile2, line2)) {
        if (line1 != line2) {
            differencesFound = true;
            std::cout << "Различие в строке " << lineNumber << ":" << std::endl;
            std::cout << "Файл 1: " << line1 << std::endl;
            std::cout << "Файл 2: " << line2 << std::endl;
        }
        ++lineNumber;
    }

    if (!differencesFound) {
        std::cout << "Файлы идентичны." << std::endl;
    }
}

int main() {
    const std::string file1 = "../assets/zad81.txt";
    const std::string file2 = "../assets/zad82.txt";

    compareFiles(file1, file2);

    return 0;
}
