#include <iostream>
#include <algorithm>

void lab41() {
    int sum = 0, zeroCount = 0, arr[9];
    float del;
    for (int i = 0; i < 9; i++) {
        std::cin >> arr[i];
        if (arr[i] > 0 && i % 2 == 0)
            sum += arr[i];
        else if (arr[i] == 0)
            zeroCount++;
    }
    double min_el = *std::min_element(std::begin(arr), std::end(arr));
    double max_el = *std::max_element(std::begin(arr), std::end(arr));
    if (min_el) {
        del = max_el / min_el;
        std::cout << max_el << "/" << min_el << " = " << del << std::endl;
    } else {
        std::cout << "min el = 0 => no solution" << std::endl;
    }
    std::cout << "sum: " << sum << std::endl << "zero count: " << zeroCount << std::endl;
}

void lab42() {
    while (true) {
        int arr[4][3];
        int maxRowSum = 0, maxRow = -1;
        for (int i = 0; i < 4; i++) {
            int rowSum = 0;
            for (int j = 0; j < 3; j++) {
                std::cin >> arr[i][j];
                rowSum += arr[i][j];
            }
            if (rowSum > maxRowSum) {
                maxRowSum = rowSum;
                maxRow = i;
            }
        }
        std::cout << maxRow << std::endl;
    }
}


int main() {
    lab41();
    //    lab42();
    return 0;
}
