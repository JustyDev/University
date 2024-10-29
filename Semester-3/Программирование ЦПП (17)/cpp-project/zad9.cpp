#include <iostream>
#include <fstream>
#include <cmath>
#include <iomanip>

void calculateCubicRoots(const std::string &inputFile, const std::string &outputFile) {
    std::ifstream inFile(inputFile);
    std::ofstream outFile(outputFile);

    if (!inFile.is_open()) {
        std::cerr << "Ошибка открытия файла: " << inputFile << std::endl;
        return;
    }

    if (!outFile.is_open()) {
        std::cerr << "Ошибка открытия файла: " << outputFile << std::endl;
        return;
    }

    double number;

    while (inFile >> number) {
        double cubicRoot = cbrt(number);
        outFile << number << ' ' << cubicRoot << std::endl;
    }
}

int main() {
    const std::string inputFile = "../assets/zad9in.txt";
    const std::string outputFile = "../assets/zad9out.txt";

    calculateCubicRoots(inputFile, outputFile);

    return 0;
}
