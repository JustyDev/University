#include <iostream>
#include <sstream>
#include <string>

bool hasLongWords(const std::string &input, int lengthThreshold) {
    std::istringstream stream(input);
    std::string word;

    while (stream >> word) {
        if (word.length() > lengthThreshold) {
            return true;
        }
    }

    return false;
}

int main() {
    std::string input = "Эта строка содержит несколько длинных слов";;
    int threshold = 50;

    if (hasLongWords(input, threshold)) {
        std::cout << "Строка содержит слово с количеством букв больше " << threshold << std::endl;
    } else {
        std::cout << "Строка не содержит слова с количеством букв больше " << threshold << std::endl;
    }

    return 0;
}
