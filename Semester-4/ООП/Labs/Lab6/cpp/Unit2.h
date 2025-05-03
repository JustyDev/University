//---------------------------------------------------------------------------
#ifndef Unit2H
#define Unit2H
#include <string.h>
#include <vcl.h>
//---------------------------------------------------------------------------

// ����� Stroka, ���������� �� ���� char
class Stroka
{
private:
    char* data;      // ��������� �� ������ ��������
    size_t length;   // ����� ������

public:
    // ����������� �� ���������
    Stroka();

    // ����������� � ����������
    Stroka(const char* str);

    // ����������� �����������
    Stroka(const Stroka& other);

    // ����������
    ~Stroka();

    // �������� ������������
    Stroka& operator=(const Stroka& other);

    // �������� �������������� �� char* � Stroka
    Stroka& operator=(const char* str);

    // �������� �������������� �� Stroka � char*
    operator const char*() const;

    // ����� ��� ��������� ������
    const char* GetStr() const;

    // ����� ��� ��������� �����
    size_t GetLength() const;
};

#endif
