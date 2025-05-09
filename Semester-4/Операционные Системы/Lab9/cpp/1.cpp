#include <iostream>
using namespace std;

void search_neg(const int*, const int*, int&);

int main() {
    int n = 0;
    cout << "Enter array length: "; cin >> n;
    int* arr1 = new int[n];
    int* arr2 = new int[n];

    cout << "Enter first array: ";
    for(int i = 0; i < n; i++) cin >> arr1[i];

    cout << "Enter second array: ";
    for(int i = 0; i < n; i++) cin >> arr2[i];

    search_neg(arr1, arr2, n);

    delete[] arr1;
    delete[] arr2;
    system("pause");
    return 0;
}

//Поиск массива с наим. кол-вом отрицательных чисел
void search_neg(const int* ar1, const int* ar2, int &len) {
    unsigned short ct1 = 0, ct2 = 0;

    for(int i = 0; i < len; i++) {
        if (ar1[i] < 0) ct1++;
        if (ar2[i] < 0) ct2++;
    }

    const char* res = (ct1 < ct2) ? "The first array has less negative digits\n" : "The second array has less negative digits\n";
    cout << res;
}