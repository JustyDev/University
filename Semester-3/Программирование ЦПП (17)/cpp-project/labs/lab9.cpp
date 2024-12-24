#include <iostream>
#include <vector>

// расположить элементы так чтобы сначала были все отрицательные потом все положительные
int main() {
    int n;
    std::cin>>n;
    std::vector<int> vec(n);
    for (int i = 0; i < n; i++)
        std::cin>>vec[i];

    int left = 0;
    int right = n - 1;

    while (left <= right) {
        if (vec[left] < 0) {
            left++;
        } else if (vec[right] >= 0) {
            right--;
        } else {
            std::swap(vec[left], vec[right]);
            left++;
            right--;
        }
    }

    for (int num : vec) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}
