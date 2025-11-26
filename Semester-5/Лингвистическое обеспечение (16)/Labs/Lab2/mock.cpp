// Примеры разных определений MYCONST
// Допускаются произвольные пробелы и табуляции.

// Должно быть: ДА (hex с U и разделителями)
#define   MYCONST     0xDEAD'BEEFu

// Десятичная — НЕТ
#define MYCONST 123
// Унарный минус + hex — НЕТ (это не один литерал)
#define MYCONST -0x2A
// Не валидный hex — НЕТ
#define MYCONST 0x1G
// Неверный суффикс — НЕТ
#define MYCONST 0xFFuz
// Скобки вокруг литерала — это ок, но это не MYCONST
#define MYCONST  (0x45LL)
// Валидный hex с суффиксами в другом порядке — это ок, но это не MYCONST
#define MYCONST  0XABC'123'0lU

// Переопределение MYCONST (если есть несколько, программа покажет все):
// ДА (скобки снимаются перед проверкой)
#define MYCONST ( 0xBADC0FFEEu )

int main() {
    return 0;
}
