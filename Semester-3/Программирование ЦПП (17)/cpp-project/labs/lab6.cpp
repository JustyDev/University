#include <iostream>
#include <cmath>
#include <stdexcept>

double mpow(double num, double x) {
    if(num==0 && x<=0) return -1;
    if(num==1 || num==0) return x;
    if(x > 1) return num * mpow(num, x-1);
    if(x < 1) return 1/num * mpow(num, x+1);
    return num;
}

void insertionSort(int* arr, int n) {
    for(int i=1; i<n; i++)
        for(int j= i;j>0 && arr[j-1]<arr[j];j--)
            std::swap(arr[j-1], arr[j]);
}

void selectionSort(int* arr, int n) {
    for (int i = 0; i < n - 1; ++i) {
        int min_ix = i;
        for (int j = i + 1; j < n; ++j)
            if (arr[j] < arr[min_ix])
                min_ix = j;

        if (min_ix != i) std::swap(arr[i], arr[min_ix]);
    }
}

void lab62() {
    while(true) {
        int n, userChoice;
        std::cin >> n;
        int arr[n];
        for(int i = 0; i <n; i++)
            std::cin>>arr[i];
        std::cout << "1 - убывание, 2 - возрастание" << std::endl;
        std::cin >> userChoice;
        if(userChoice==1) {
            insertionSort(arr, n);
            for(int i = 0; i<n; i++) std::cout<<arr[i] << " ";
        }
        else if(userChoice==2) {
            selectionSort(arr, n);
            for(int i = 0; i<n; i++) std::cout<<arr[i] << " ";
        } else std::cout<<"wrong input" << std::endl;
        std::cout<<std::endl;
    }
}

void lab63() {
    std::string s;
    std::cin >> s;
    for(int i = 0; i<s.length()/2; i++) {
        std::swap(s[i], s[s.length()-1-i]);
    }
    std::cout<<s<<std::endl;
}

int solve(double a, double b, double c, double &x1, double &x2) {
    try {
        if (a == 0) {
            throw std::invalid_argument("a не должно быть равно нулю.");
        }

        double d = b * b - 4 * a * c;

        if (d > 0) {
            x1 = (-b + sqrt(d)) / (2 * a);
            x2 = (-b - sqrt(d)) / (2 * a);
            return 2;
        } else if (d == 0) {
            x1 = x2 = -b / (2 * a);
            return 1;
        } else
            return 0;
    } catch (const std::invalid_argument &e) {
        std::cerr << "Ошибка: " << e.what() << std::endl;
        return -1;
    }
}

void lab64() {
    double a, b, c;
    double x1, x2;

    std::cin >> a >> b >> c;

    int result = solve(a, b, c, x1, x2);

    if (result == 2)
        std::cout << "Два корня: " << x1 << ", " << x2 << std::endl;
    else if (result == 1)
        std::cout << "Один корень: " << x1 << std::endl;
    else if (result == 0)
        std::cout << "не имеет действительных корней." << std::endl;
    else
        std::cout << "некорректный ввод" << std::endl;
}

int main() {
    //std::cout << mpow(2, 3); // lab 61
   // lab62();
    //lab63();
    lab64();
    return 0;
}
