#include <vcl.h>
#pragma hdrstop

#include "Unit2.h"
#include "Unit1.h"

#pragma package(smart_init)

int ProductType = 0;

float Tovar::get_price() {
    return price;
}

void Tovar::add_rec() {
    if (ProductType == 0) {
        strcpy(name, AnsiString(Form1->LabeledEdit1->Text).c_str());
        number = StrToInt(Form1->LabeledEdit2->Text);
        price = StrToFloat(Form1->LabeledEdit3->Text);
    }
    if (ProductType == 1) {
        strcpy(name, AnsiString(Form1->LabeledEdit6->Text).c_str());
        number = StrToInt(Form1->LabeledEdit7->Text);
        price = StrToFloat(Form1->LabeledEdit8->Text);
    }
}

void Tovar::show() {
    AnsiString s = AnsiString(name) + "|" + IntToStr(number) + "|" + FloatToStr(price);
    Form1->Memo1->Lines->Add(s);
}


void TovarProd::add_rec() {
    Tovar::add_rec();
    term = StrToInt(Form1->LabeledEdit4->Text);
    temp = StrToInt(Form1->LabeledEdit5->Text);
}

void TovarProd::show() {
    Tovar::show();
    AnsiString s2 = IntToStr(term) + "|" + IntToStr(temp);
    Form1->Memo1->Lines->Add(s2);
}

