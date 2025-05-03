//---------------------------------------------------------------------------
#ifndef Unit2H
#define Unit2H
#include <string.h>
#include <vcl.h>
//---------------------------------------------------------------------------

// Класс Stroka, основанный на типе char
class Stroka
{
private:
    char* data;      // Указатель на строку символов
    size_t length;   // Длина строки

public:
    // Конструктор по умолчанию
    Stroka();

    // Конструктор с параметром
    Stroka(const char* str);

    // Конструктор копирования
    Stroka(const Stroka& other);

    // Деструктор
    ~Stroka();

    // Оператор присваивания
    Stroka& operator=(const Stroka& other);

    // Оператор преобразования из char* в Stroka
    Stroka& operator=(const char* str);

    // Оператор преобразования из Stroka в char*
    operator const char*() const;

    // Метод для получения строки
    const char* GetStr() const;

    // Метод для получения длины
    size_t GetLength() const;
};

#endif
