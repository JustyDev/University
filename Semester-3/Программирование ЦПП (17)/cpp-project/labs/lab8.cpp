#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

void displayFileContent() {
    std::ifstream file("/Users/justy-dev/Documents/GitHub/University/Semester-3/Программирование ЦПП (17)/cpp-project/assets/lab8in.txt");
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line))
            std::cout << line << std::endl;
        file.close();

    } else {
        std::cout << "no such file" << std::endl;
        return;
    }
}


void extractSentencesWithWord(const std::string& word) {
    std::ifstream file("/Users/justy-dev/Documents/GitHub/University/Semester-3/Программирование ЦПП (17)/cpp-project/assets/lab8in.txt");
    if (!file.is_open()) {
        std::cout << "no such file" << std::endl;
        return;
    }

    std::string text((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    file.close();

    std::vector<std::string> sentences;
    std::istringstream stream(text);
    std::string sentence;
    bool wordFound = false;

    // Разделяем текст на предложения
    while (std::getline(stream, sentence, '.')) {
        if (sentence.find(word) != std::string::npos) {
            wordFound = true;
            sentences.push_back(sentence + '.');
        }
    }

    if (!wordFound) {
        std::cout << "Слово \"" << word << "\" отсутствует в тексте." << std::endl;
        return;
    }

    std::ofstream outFile("/Users/justy-dev/Documents/GitHub/University/Semester-3/Программирование ЦПП (17)/cpp-project/assets/lab8out.txt");
    if (!outFile.is_open()) {
        std::cout << "no such file" << std::endl;
        return;
    }

    for (const auto& s : sentences) {
        outFile << s << std::endl;
    }

    std::cout << word << " записаны в файл." << std::endl;
    outFile.close();
}

int main() {
    std::string word;
    std::cout << "Содержимое файла:" << std::endl;
    displayFileContent();

    std::cout << "\nВведите слово для поиска: ";
    std::cin >> word;

    extractSentencesWithWord(word);

    return 0;
}
