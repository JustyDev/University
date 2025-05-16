#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    const int SIZE = 10;
    vector<int> arr(SIZE);
    int n, counter = 0;

    cout << "Введите 10 чисел через пробел: ";
    for (int i = 0; i < SIZE; i++) {
        cin >> arr[i];
    }

    cout << "Введите число для поиска в массиве: ";
    cin >> n;

    counter = count_if(arr.begin(), arr.end(), [n](int num){
        return n == num;
    });
    cout << "Кол-во совпадений: " << counter << '\n';
    
    system("pause");
    return 0;
}