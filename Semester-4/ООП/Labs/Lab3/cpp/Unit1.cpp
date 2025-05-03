//---------------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;

void MyTime::show(){
    AnsiString s;
    s = IntToStr(chas) + ":" + IntToStr(min) + ":" + IntToStr(sec);
    Form1->Memo1->Lines->Add(s);
}

void MyTime::summa(MyTime t1, MyTime t2){
    sec = t1.sec + t2.sec;
    min = t1.min + t2.min;
    chas = t1.chas + t2.chas;
    if(sec>=60) { min++; sec-=60; }
    if(min>=60) { chas++; min-=60; }
    if(chas>=24) chas = chas-24;
}

bool MyTime::parseTimeString(const AnsiString &timeStr) {
    try {
        // Проверяем формат ЧЧ:ММ:СС
        if (timeStr.Length() != 8 || timeStr[3] != ':' || timeStr[6] != ':')
            return false;

        chas = StrToInt(timeStr.SubString(1, 2));
        min = StrToInt(timeStr.SubString(4, 2));
        sec = StrToInt(timeStr.SubString(7, 2));

        // Проверка допустимых диапазонов
        if (chas < 0 || chas > 23 || min < 0 || min > 59 || sec < 0 || sec > 59)
            return false;

        return true;
    }
    catch (...) {
        return false; // Ошибка преобразования строки в число
    }
}

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
    : TForm(Owner)
{
    // Устанавливаем подсказку для полей ввода
    LabeledEdit1->TextHint = "ЧЧ:ММ:СС";
    LabeledEdit2->TextHint = "ЧЧ:ММ:СС";
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
    Memo1->Clear();
    MyTime T1, T2, T3;

    // Проверяем корректность ввода времени 1
    if (!T1.parseTimeString(LabeledEdit1->Text)) {
        ShowMessage("Ошибка в формате времени 1. Используйте формат ЧЧ:ММ:СС");
        LabeledEdit1->SetFocus();
        return;
    }

    // Проверяем корректность ввода времени 2
    if (!T2.parseTimeString(LabeledEdit2->Text)) {
        ShowMessage("Ошибка в формате времени 2. Используйте формат ЧЧ:ММ:СС");
        LabeledEdit2->SetFocus();
        return;
    }

    T1.show();
    T2.show();
    T3.summa(T1, T2);
    T3.show();
}

//---------------------------------------------------------------------------
void __fastcall TForm1::Button2Click(TObject *Sender)
{
	Memo1->Clear();

	// Парсим введенные пользователем данные для создания объектов
try {
		// Разбор строки для T1
		AnsiString str1 = LabeledEdit1->Text;
		if (str1.Length() != 8 || str1[3] != ':' || str1[6] != ':') {
			ShowMessage("Ошибка в формате времени 1. Используйте формат ЧЧ:ММ:СС");
			LabeledEdit1->SetFocus();
			return;
		}

		int ch1 = StrToInt(str1.SubString(1, 2));
		int min1 = StrToInt(str1.SubString(4, 2));
		int sec1 = StrToInt(str1.SubString(7, 2));

		// Проверка диапазонов для T1
		if (ch1 < 0 || ch1 > 23 || min1 < 0 || min1 > 59 || sec1 < 0 || sec1 > 59) {
			ShowMessage("Некорректные значения времени 1");
			LabeledEdit1->SetFocus();
			return;
		}

		// Разбор строки для T2
		AnsiString str2 = LabeledEdit2->Text;
		if (str2.Length() != 8 || str2[3] != ':' || str2[6] != ':') {
			ShowMessage("Ошибка в формате времени 2. Используйте формат ЧЧ:ММ:СС");
			LabeledEdit2->SetFocus();
			return;
		}

		int ch2 = StrToInt(str2.SubString(1, 2));
        int min2 = StrToInt(str2.SubString(4, 2));
        int sec2 = StrToInt(str2.SubString(7, 2));

        // Проверка диапазонов для T2
        if (ch2 < 0 || ch2 > 23 || min2 < 0 || min2 > 59 || sec2 < 0 || sec2 > 59) {
            ShowMessage("Некорректные значения времени 2");
			LabeledEdit2->SetFocus();
            return;
        }

        // Создаем объекты через конструктор с параметрами
        MyTime T1(ch1, min1, sec1);
        MyTime T2(ch2, min2, sec2);
        MyTime T3;

        // Отображаем результаты
        T1.show();
		T2.show();
        T3.summa(T1, T2);
        T3.show();
    }
    catch (...) {
        ShowMessage("Ошибка при обработке введенных данных");
    }
}
