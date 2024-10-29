#include <iostream>
#include <cmath>

void lab11() {
    int inp;
    std::cin >> inp;
    std::cout << inp * 0.4059 << "kg";
}

void lab12() {
    double alpha;
    std::cin >> alpha;
    alpha = alpha * M_PI / 180;
    const double z1 = (1 - 2 * pow(sin(alpha), 2)) / (1 + sin(alpha * 2));
    const double z2 = (1 - tan(alpha)) / (1 + tan(alpha));

    std::cout << z1 << " " << z2;
}

int main() {
    // lab11();
    lab12();
    return 0;
}
