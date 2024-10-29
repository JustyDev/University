#include <iostream>

// вычислить значение функции

double calculateFunctionSwitch(int X) {
    switch (X) {
        case 5:
        case 3:
            return exp(X);
        case 10:
            return 3 + 11212 * X;
        default:
            return X * X * 2;
    }
}

double calculateFunctionIf(int X) {
    if (X == 5 || X == 3) {
        return exp(X);
    }
    if (X == 10) {
        return 3 + 11212 * X;
    }
    return X * X * 2;
}

void withIf() {
    std::cout << "X\tf(X)" << std::endl;
    for (int X = -1; X <= 20; ++X) {
        double result = calculateFunctionIf(X);
        std::cout << X << "\t" << result << std::endl;
    }
}

void withSwitch() {
    std::cout << "X\tf(X)" << std::endl;
    for (int X = -1; X <= 20; ++X) {
        double result = calculateFunctionSwitch(X);
        std::cout << X << "\t" << result << std::endl;
    }
}

int main() {
    withIf();
    // withSwitch();

    return 0;
}
