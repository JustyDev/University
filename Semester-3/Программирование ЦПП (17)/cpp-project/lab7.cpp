#include <iostream>
#include <limits.h>
#include <map>

int findMinSum(int* arr, int& size) {
    if (size < 2) {
        std::cout << "<2 el" << std::endl;
        return -1;
    }
    int minSum = INT_MAX;
    for (int i = 0; i < size - 1; ++i) {
        int sum = arr[i] + arr[i + 1];
        if (sum < minSum)
            minSum = sum;
    }
    return minSum;
}

int lab71() {
    int size;
    std::cin >> size;

    if (size < 2) {
        std::cout << "<2 el" << std::endl;
        return -1;
    }

    int* arr = new int[size];

    for (int i = 0; i < size; ++i)
        std::cin >> arr[i];

    int minSum = findMinSum(arr, size);
    delete[] arr;
    return minSum;
}


void printMatrix(int** matrix, int m, int n) {
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j)
            std::cout << matrix[i][j] << " ";
        std::cout << std::endl;
    }
}

// Функция для вычисления суммы строк с отрицательными элементами
int sumNegativem(int** matrix, int m, int n) {
    int totalSum = 0;
    for (int i = 0; i < m; ++i) {
        bool hasNegative = false;
        int mum = 0;
        for (int j = 0; j < n; ++j) {
            mum += matrix[i][j];
            if (matrix[i][j] < 0) {
                hasNegative = true;
            }
        }
        if (hasNegative) {
            totalSum += mum;
        }
    }
    return totalSum;
}


int findMinDuplicate(int** matrix, int m, int n) {
    std::map<int, int> elementCount;
    int minDuplicate = INT_MAX;

    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            elementCount[matrix[i][j]]++;


    for (const auto& pair : elementCount)
        if (pair.second > 1)
            if (pair.first < minDuplicate)
                minDuplicate = pair.first;


    if (minDuplicate == INT_MAX)
        return -1;


    return minDuplicate;
}

void lab72() {
    int m, n;
    std::cin >> m;
    std::cin >> n;

    int** matrix = new int*[m];
    for (int i = 0; i < m; ++i) {
        matrix[i] = new int[n];
    }

    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            std::cin >> matrix[i][j];

    printMatrix(matrix, m, n);

    int negativemSum = sumNegativem(matrix, m, n);
    std::cout << "Сумма элементов строк с отрицательными элементами: " << negativemSum << std::endl;

    int minDuplicate = findMinDuplicate(matrix, m, n);
    if (minDuplicate == -1)
        std::cout << "В матрице нет дублирующихся элементов." << std::endl;
    else
        std::cout << "Минимальный дубликат в матрице: " << minDuplicate << std::endl;


    for (int i = 0; i < m; ++i)
        delete[] matrix[i];
    delete[] matrix;
}



int main() {
    // std::cout<<lab71();
    lab72();
    return 0;
}
