#include <iostream>
#include <fstream>

struct Recorder {
    char firmName[10];
    char modelName[10];
    uint16_t outputPower;
    uint16_t energyConsumption;
    uint32_t price;
};

const int RECORD_SIZE = sizeof(Recorder);

void writeRecord(const std::string &filename, const Recorder &recorder, int recordNumber) {
    std::ofstream outFile(filename, std::ios::binary | std::ios::in | std::ios::out);
    if (!outFile) {
        std::cerr << "Ошибка открытия файла для записи!" << std::endl;
        return;
    }

    outFile.seekp(recordNumber * RECORD_SIZE);
    outFile.write(reinterpret_cast<const char *>(&recorder), RECORD_SIZE);
}

void readRecord(const std::string &filename, Recorder &recorder, int recordNumber) {
    std::ifstream inFile(filename, std::ios::binary);
    if (!inFile) {
        std::cerr << "Ошибка открытия файла для чтения!" << std::endl;
        return;
    }

    inFile.seekg(recordNumber * RECORD_SIZE);
    inFile.read(reinterpret_cast<char *>(&recorder), RECORD_SIZE);
}

int main() {
    const std::string filename = "../assets/zad10.dat";

    Recorder recorder1 = {"Sony", "ModelX", 100, 50, 2999};

    writeRecord(filename, recorder1, 0);

    Recorder readRecorder;
    readRecord(filename, readRecorder, 0);

    std::cout << "Прочитанная запись:" << std::endl;
    std::cout << "Фирма: " << readRecorder.firmName << std::endl;
    std::cout << "Модель: " << readRecorder.modelName << std::endl;
    std::cout << "Выходная мощность: " << readRecorder.outputPower << std::endl;
    std::cout << "Потребление энергии: " << readRecorder.energyConsumption << std::endl;
    std::cout << "Цена: " << readRecorder.price << std::endl;

    return 0;
}
