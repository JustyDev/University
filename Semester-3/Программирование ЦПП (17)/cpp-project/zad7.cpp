
#include <iostream>

void findMinMax(int matrix[][3], int n, int &minElement, int &maxElement) {
    minElement = INT_MAX;
    maxElement = INT_MIN;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (matrix[i][j] < minElement) {
                minElement = matrix[i][j];
            }
            if (matrix[i][j] > maxElement) {
                maxElement = matrix[i][j];
            }
        }
    }
}

int main() {
    const int N = 3;

    int matrix[N][N] = {
        {3, 5, 9},
        {1, 6, 7},
        {8, 2, 4}
    };

    int minElement, maxElement;
    findMinMax(matrix, N, minElement, maxElement);

    std::cout << "Минимальный элемент: " << minElement << std::endl;
    std::cout << "Максимальный элемент: " << maxElement << std::endl;

    return 0;
}
