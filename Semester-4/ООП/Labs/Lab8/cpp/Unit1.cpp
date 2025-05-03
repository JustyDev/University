//---------------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;

FloatPr::FloatPr() : Float() {}

FloatPr::FloatPr(float v) : Float(v) {}

FloatPr::FloatPr(Float a) : Float(a) {}

FloatPr FloatPr::operator-(FloatPr b) {
    return FloatPr(f - b.f);
}

FloatPr FloatPr::operator*(FloatPr b) {
    return FloatPr(f * b.f);
}

FloatPr FloatPr::operator/(FloatPr b) {
    if (b.f == 0) {
        throw Exception("Деление на ноль невозможно!");
    }
    return FloatPr(f / b.f);
}

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
    : TForm(Owner)
{
}
//---------------------------------------------------------------------------

bool TForm1::ValidateInput()
{
    try {
        StrToFloat(LabeledEdit1->Text);
        StrToFloat(LabeledEdit2->Text);
        return true;
    }
    catch (Exception &e) {
        Panel1->Caption = "Ошибка ввода: введите числовые значения";
        return false;
    }
}

void __fastcall TForm1::Button1Click(TObject *Sender)
{
    try {
        if (!ValidateInput()) return;

        FloatPr f1, f2, f3;
        f1 = StrToFloat(LabeledEdit1->Text);
        f2 = StrToFloat(LabeledEdit2->Text);
        f3 = f1 + f2;
        f3.show(Panel1);
    }
    catch (Exception &e) {
        Panel1->Caption = e.Message;
    }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button2Click(TObject *Sender)
{
    try {
        if (!ValidateInput()) return;

        FloatPr f1, f2, f3;
        f1 = StrToFloat(LabeledEdit1->Text);
        f2 = StrToFloat(LabeledEdit2->Text);
        f3 = f1 - f2;
        f3.show(Panel1);
    }
    catch (Exception &e) {
        Panel1->Caption = e.Message;
    }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button3Click(TObject *Sender)
{
    try {
        if (!ValidateInput()) return;

        FloatPr f1, f2, f3;
        f1 = StrToFloat(LabeledEdit1->Text);
        f2 = StrToFloat(LabeledEdit2->Text);
        f3 = f1 * f2;
        f3.show(Panel1);
    }
    catch (Exception &e) {
		Panel1->Caption = e.Message;
	}
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button4Click(TObject *Sender)
{
    try {
        if (!ValidateInput()) return;

        FloatPr f1, f2, f3;
        f1 = StrToFloat(LabeledEdit1->Text);
        f2 = StrToFloat(LabeledEdit2->Text);
		f3 = f1 / f2;
        f3.show(Panel1);
	}
    catch (Exception &e) {
        Panel1->Caption = e.Message;
    }
}
