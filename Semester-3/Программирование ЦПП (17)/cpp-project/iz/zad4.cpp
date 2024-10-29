#include <iostream>

void swapSecondAndLast(char *str) {
    char *words[100];
    int index = 0;
    bool inWord = false;
    int wordStart = 0;

    for (int i = 0; str[i] != '\0'; ++i) {
        if (str[i] != ' ' && !inWord) {
            inWord = true;
            wordStart = i;
        }

        if ((str[i] == ' ' || str[i + 1] == '\0') && inWord) {
            int length = (str[i + 1] == '\0') ? i - wordStart + 1 : i - wordStart;
            words[index] = new char[length + 1];

            for (int j = 0; j < length; ++j) {
                words[index][j] = str[wordStart + j];
            }
            words[index][length] = '\0';
            inWord = false;
            index++;
        }
    }

    if (index > 1) {
        char *temp = words[1];
        words[1] = words[index - 1];
        words[index - 1] = temp;
    }

    int pos = 0;
    for (int i = 0; i < index; ++i) {
        int j = 0;
        while (words[i][j] != '\0') {
            str[pos++] = words[i][j++];
        }

        if (i < index - 1) {
            str[pos++] = ' ';
        }

        delete[] words[i];
    }
    str[pos] = '\0';
}

int main() {
    char str[] = "Это пример строки для замены слов";

    std::cout << "Исходная строка: " << str << std::endl;

    swapSecondAndLast(str);

    std::cout << "Изменённая строка: " << str << std::endl;

    return 0;
}
