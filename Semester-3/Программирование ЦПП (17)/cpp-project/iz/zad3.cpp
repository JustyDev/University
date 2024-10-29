#include <iostream>

int main() {
    int N;
    std::cout << "Введите целое число N: ";
    std::cin >> N;

    std::string number = std::to_string(abs(N));
    int maxDifference = 0;

    for (size_t i = 0; i < number.length() - 1; ++i) {
        int digit1 = number[i] - '0';
        int digit2 = number[i + 1] - '0';
        int difference = abs(digit1 - digit2);

        if (difference > maxDifference) {
            maxDifference = difference;
        }
    }

    std::cout << "Максимальная разность между двумя соседними цифрами: " << maxDifference << std::endl;

    return 0;
}
