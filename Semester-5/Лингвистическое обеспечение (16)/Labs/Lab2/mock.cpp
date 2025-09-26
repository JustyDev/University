// Примеры разных определений MYCONST
// Допускаются произвольные пробелы и табуляции.
#define   MYCONST     0xDEAD'BEEFu     // Должно быть: ДА (hex с U и разделителями)

#define MYCONST_BAD1 123               // Десятичная — НЕТ
#define MYCONST_BAD2 -0x2A             // Унарный минус + hex — НЕТ (это не один литерал)
#define MYCONST_BAD3 0x1G              // Не валидный hex — НЕТ
#define MYCONST_BAD4 0xFFuz            // Неверный суффикс — НЕТ
#define MYCONST_OK2  (0x45LL)          // Скобки вокруг литерала — это ок, но это не MYCONST
#define MYCONST_OK3  0XABC'123'0lU     // Валидный hex с суффиксами в другом порядке — это ок, но это не MYCONST

// Переопределение MYCONST (если есть несколько, программа покажет все):
#define MYCONST ( 0xBADC0FFEEu )       // ДА (скобки снимаются перед проверкой)

int main() {
    return 0;
}
