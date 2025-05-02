//---------------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;


// Проверка валидности введенных значений
bool __fastcall TForm1::IsInputValid()
{
	// Проверяем, что поля не пустые
	if (LabeledEdit1->Text.Trim() == "" || LabeledEdit2->Text.Trim() == "") {
		return false;
	}

	try {
		// Проверяем, что введены числа
		int val1 = StrToInt(LabeledEdit1->Text);
		int val2 = StrToInt(LabeledEdit2->Text);
        return true;
	}
	catch (EConvertError &e) {
		// Если возникла ошибка конвертации - значит введены не числа
		return false;
	}
}

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
UpdateButtonsState();
}

// Обновление состояния кнопок
void __fastcall TForm1::UpdateButtonsState()
{
    bool isValid = IsInputValid();

    // Обновляем состояние всех кнопок операций
    Button1->Enabled = isValid;
    Button2->Enabled = isValid;
    Button3->Enabled = isValid;
    Button4->Enabled = isValid;
    Button5->Enabled = isValid;
    Button6->Enabled = isValid;
}

// Обработчик изменения текста в первом поле ввода
void __fastcall TForm1::LabeledEdit1Change(TObject *Sender)
{
    UpdateButtonsState();
}

//---------------------------------------------------------------------------
// Обработчик изменения текста во втором поле ввода
void __fastcall TForm1::LabeledEdit2Change(TObject *Sender)
{
    UpdateButtonsState();
}

class MyInt {
	private:
		int I;
	public:
		MyInt() { I=0; }
		MyInt(int i) { I=i; }
		void show(){
			Form1->Memo1->Lines->Add(I);
		}

		// Оператор сложения (уже есть)
		MyInt operator+(MyInt a2) {
			return (I + a2.I);
		}

		// Оператор вычитания
		MyInt operator-(MyInt a2) {
			return (I - a2.I);
		}

		// Оператор умножения
        MyInt operator*(MyInt a2) {
            return (I * a2.I);
        }

        // Оператор деления
		MyInt operator/(MyInt a2) {
            if (a2.I == 0) {
                Form1->Memo1->Lines->Add("Ошибка: деление на ноль!");
                return 0;
            }
			return (I / a2.I);
        }

		// Оператор сравнения < (уже есть)
		bool operator<(MyInt a2) {
			if(I < a2.I) return true;
			else return false;
		}

		// Оператор равенства
        bool operator==(MyInt a2) {
            return (I == a2.I);
        }
};

//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	// Сложение
	MyInt i1, i2, i3;
	i1 = StrToInt(LabeledEdit1->Text);
	i2 = StrToInt(LabeledEdit2->Text);
	i3 = i1 + i2;
	i3.show();
}

void __fastcall TForm1::Button2Click(TObject *Sender)
{
    // Вычитание
    MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
	i3 = i1 - i2;
    i3.show();
}

void __fastcall TForm1::Button3Click(TObject *Sender)
{
    // Умножение
    MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
    i3 = i1 * i2;
    i3.show();
}

void __fastcall TForm1::Button4Click(TObject *Sender)
{
    // Деление
    MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
    i3 = i1 / i2;
    i3.show();
}

void __fastcall TForm1::Button5Click(TObject *Sender)
{
	// Сравнение <
	MyInt i1, i2, i3;
    i1 = StrToInt(LabeledEdit1->Text);
    i2 = StrToInt(LabeledEdit2->Text);
    if(i1 < i2) Form1->Memo1->Lines->Add("Истина");
    else Form1->Memo1->Lines->Add("ЛОЖЬ");
}

void __fastcall TForm1::Button6Click(TObject *Sender)
{
	// Сравнение ==
	MyInt i1, i2, i3;
	i1 = StrToInt(LabeledEdit1->Text);
	i2 = StrToInt(LabeledEdit2->Text);
	if(i1 == i2) Form1->Memo1->Lines->Add("Истина");
	else Form1->Memo1->Lines->Add("ЛОЖЬ");
}

void __fastcall TForm1::Button7Click(TObject *Sender)
{
	Form1->Memo1->Clear();
}
