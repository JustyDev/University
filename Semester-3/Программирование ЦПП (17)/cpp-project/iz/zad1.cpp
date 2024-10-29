#include <iostream>
#include <cmath>

// 1, 3, -4
// ответ будет 1, -4

int main() {
    double a, b, c;

    std::cout << "Введите коэффициенты a, b и c: ";
    std::cin >> a >> b >> c;

    if (a == 0) {
        std::cout << "Это не квадратное уравнение, так как a = 0." << std::endl;
        return 1;
    }

    double discriminant = b * b - 4 * a * c;

    if (discriminant > 0) {
        double root1 = (-b + sqrt(discriminant)) / (2 * a);
        double root2 = (-b - sqrt(discriminant)) / (2 * a);

        std::cout << "Уравнение имеет два различных вещественных корня: " << std::endl;
        std::cout << "x1 = " << root1 << std::endl;
        std::cout << "x2 = " << root2 << std::endl;
    } else if (discriminant == 0) {
        double root = -b / (2 * a);
        std::cout << "Уравнение имеет один вещественный корень: " << std::endl;
        std::cout << "x = " << root << std::endl;
    } else {
        // комплексные числа не нужны
        std::cout << "Уравнение не имеет решения в вещественных числах" << std::endl;
    }

    return 0;
}
