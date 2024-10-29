#include <iostream>
#include <cstring> // Для работы со стандартными строковыми функциями

bool hasLongWords(const char *str, size_t limit) {
    const char *delimiters = " ";
    char *strCopy = new char[strlen(str) + 1];
    strcpy(strCopy, str);

    char *token = strtok(strCopy, delimiters);
    while (token != nullptr) {
        if (strlen(token) > limit) {
            delete[] strCopy;
            return true;
        }
        token = strtok(nullptr, delimiters);
    }

    delete[] strCopy;
    return false;
}

int main() {
    const char *sentence = "Эта строка содержит несколько длинных слов";
    size_t limit = 5;

    if (hasLongWords(sentence, limit)) {
        std::cout << "В строке есть слова, длинее заданного числа" << std::endl;
    } else {
        std::cout << "В строке нет слов, длиннее заданного числа" << std::endl;
    }

    return 0;
}
