//---------------------------------------------------------------------------

#include <vcl.h>
#include "Unit2.h"
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner) : TForm(Owner)
{
	ShuffleData();
    DrawData(PaintBox1);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	ShuffleData();
	DrawData(PaintBox1);

    int index = ComboBox1->ItemIndex;
    SortType type = static_cast<SortType>(index);
    Sort(type, PaintBox1);
}
//---------------------------------------------------------------------------
