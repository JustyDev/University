
#include <iostream>

int digitSum(int num) {
    int sum = 0;
    num = abs(num); // Учитываем отрицательные числа
    while (num > 0) {
        sum += num % 10;
        num /= 10;
    }
    return sum;
}

void sortByDigitSum(int* arr, int size) {
    for (int i = 0; i < size - 1; ++i) {
        for (int j = 0; j < size - i - 1; ++j) {
            if (digitSum(arr[j]) < digitSum(arr[j + 1])) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

int main() {
    int arr[] = {293, 14, 59, 102, 75};
    int size = sizeof(arr) / sizeof(arr[0]);

    sortByDigitSum(arr, size);

    std::cout << "Отсортированный массив: ";
    for (int i = 0; i < size; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}
