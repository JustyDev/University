//---------------------------------------------------------------------------
#pragma hdrstop

#include "Unit2.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)

// ����������� �� ���������
Stroka::Stroka() : data(nullptr), length(0)
{
    data = new char[1];
    data[0] = '\0';
}

// ����������� � ����������
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

// ����������� �����������
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

// ����������
Stroka::~Stroka()
{
    delete[] data;
}

// �������� ������������
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

// �������� �������������� �� char* � Stroka
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

// �������� �������������� �� Stroka � char*
Stroka::operator const char*() const
{
    return data;
}

// ����� ��� ��������� ������
const char* Stroka::GetStr() const
{
    return data;
}

// ����� ��� ��������� �����
size_t Stroka::GetLength() const
{
    return length;
}
