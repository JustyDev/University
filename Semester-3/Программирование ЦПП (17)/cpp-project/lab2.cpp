#include <iostream>
#include <iomanip>

double y(const int x) {
    return 2 * x * x - 5 * x - 8;
}

void lab21() {
    double diapStart, diapEnd, diapSteps;
    std::cin >> diapStart >> diapEnd >> diapSteps;
    std::cout << "|   x   |    y    |" << std::endl;
    std::cout << "-------------------" << std::endl;

    for (double i = diapStart; i <= diapEnd; i += diapSteps) {
        std::cout << std::setw(6) << std::fixed << std::setprecision(1) << i
                << std::setw(10) << std::fixed << std::setprecision(1) << y(i)
                << std::endl;
    }
}

void lab22() {
    int n, i = 0, sum = 0;
    std::cin >> n;
    std::string n_str = std::to_string(n);
    while (i < n_str.length()) {
        sum += n_str[i++] - '0';
    }
    std::cout << sum;
}

int main() {
    // lab21();
    lab22();
    return 0;
}
