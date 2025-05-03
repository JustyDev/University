//---------------------------------------------------------------------------
#pragma hdrstop

#include "Unit2.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)

// Конструктор по умолчанию
Stroka::Stroka() : data(nullptr), length(0)
{
    data = new char[1];
    data[0] = '\0';
}

// Конструктор с параметром
Stroka::Stroka(const char* str) : data(nullptr), length(0)
{
    if (str) {
        length = strlen(str);
        data = new char[length + 1];
        strcpy(data, str);
    } else {
        data = new char[1];
        data[0] = '\0';
    }
}

// Конструктор копирования
Stroka::Stroka(const Stroka& other) : data(nullptr), length(other.length)
{
    if (other.data) {
        data = new char[length + 1];
        strcpy(data, other.data);
    } else {
        data = new char[1];
        data[0] = '\0';
    }
}

// Деструктор
Stroka::~Stroka()
{
    delete[] data;
}

// Оператор присваивания
Stroka& Stroka::operator=(const Stroka& other)
{
    if (this != &other) {
        delete[] data;
        length = other.length;
        if (other.data) {
            data = new char[length + 1];
            strcpy(data, other.data);
        } else {
            data = new char[1];
            data[0] = '\0';
        }
    }
    return *this;
}

// Оператор преобразования из char* в Stroka
Stroka& Stroka::operator=(const char* str)
{
    delete[] data;
    if (str) {
        length = strlen(str);
        data = new char[length + 1];
        strcpy(data, str);
    } else {
        length = 0;
        data = new char[1];
        data[0] = '\0';
    }
    return *this;
}

// Оператор преобразования из Stroka в char*
Stroka::operator const char*() const
{
    return data;
}

// Метод для получения строки
const char* Stroka::GetStr() const
{
    return data;
}

// Метод для получения длины
size_t Stroka::GetLength() const
{
    return length;
}
