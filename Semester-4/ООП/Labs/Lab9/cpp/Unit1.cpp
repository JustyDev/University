//---------------------------------------------------------------------------

#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
#include "Unit2.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;

const int K = 200;
Tovar* pTovar [K];
int itemCount = 0;
//---------------------------------------------------------------------------

void __fastcall TForm1::Button2Click(TObject *Sender)
{
	if (itemCount >= K) return;
    ProductType = 1;
    pTovar[itemCount] = new TovarProm();
    pTovar[itemCount]->add_rec();
    pTovar[itemCount]->show();
    itemCount++;
}
//---------------------------------------------------------------------------

void __fastcall TForm1::FormClose(TObject *Sender, TCloseAction &Action)
{
    for (int i = 0; i < itemCount; i++) {
        delete pTovar[i];
    }
    itemCount = 0;
}

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	if (itemCount >= K) return;
    ProductType = 0;
    pTovar[itemCount] = new TovarProd();
    pTovar[itemCount]->add_rec();
    pTovar[itemCount]->show();
    itemCount++;
}


void __fastcall TForm1::Button3Click(TObject *Sender)
{
	if (itemCount == 0) {
		ShowMessage(L"Нет товаров!");
	} else {
		float sum = 0.0;

		for (int i = 0; i < itemCount; i++) {
			sum += pTovar[i]->get_price();
		}

		ShowMessage(L"Общая стоимость товаров: " + FloatToStr(sum));
	}
}
//---------------------------------------------------------------------------

