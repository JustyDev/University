#include <iostream>
#include <iomanip>

std::string lab31() {
    int x, y;
    std::cin >> x >> y;
    const bool inLeftCircle = std::pow(x + 1, 2) + std::pow(y, 2) <= 1;
    const bool inRightCircle = std::pow(x - 1, 2) + std::pow(y, 2) <= 1;

    if (inLeftCircle && inRightCircle)
        return "DA";
    return "NET";
}

void printRow(int x, double y) {
    std::cout << std::setw(5) << std::fixed << std::setprecision(1) << x
            << std::setw(11) << std::fixed << std::setprecision(1) << y
            << std::endl;
}

void lab32_if() {
    int x, y;
    std::cin >> x;
    std::cout << "|   x   |    y    |" << std::endl;
    std::cout << "-------------------" << std::endl;
    if (x == 5 || x == 10)
        for (int i = 1; i <= 10; i++) {
            y = 2 * i * i + 10;
            printRow(i, y);
        }
    else if (x == 1)
        for (int i = 1; i <= 10; i += 1) {
            y = pow(4 * i, -2) + pow(27 * i, -3) - i;
            printRow(i, y);
        }
    else
        for (int i = 1; i <= 10; i += 1) {
            y = (-1) / i;
            printRow(10, y);
        }
}

void lab32_switch() {
    int x, y;
    std::cin >> x;
    std::cout << "|   x   |    y    |" << std::endl;
    std::cout << "-------------------" << std::endl;
    switch (x) {
        case 5:
        case 10: for (int i = 1; i <= 10; i++) {
                y = 2 * i * i + 10;
                printRow(i, y);
            };
            break;
        case 1: for (int i = 1; i <= 10; i += 1) {
                y = pow(4 * i, -2) + pow(27 * i, -3) - i;
                printRow(i, y);
            };
            break;
        default: for (int i = 1; i <= 10; i += 1) {
                y = (-1) / i;
                printRow(10, y);
            };
            break;
    }
}


int main() {
    //std::cout << lab31();
    // lab32_if();
    lab32_switch();
    return 0;
}
