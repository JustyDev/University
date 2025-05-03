//---------------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
    : TForm(Owner)
{
	Caption = "ÑÒÄ-ÀÒÄ-ÑÒÄ";
	Label1->Caption = "Ââåäèòå ñòðîêó";
}
//---------------------------------------------------------------------------
void __fastcall TForm1::CTDtoATDButtonClick(TObject *Sender)
{
    AnsiString inputStr = InputEdit->Text;
    const char* stdString = inputStr.c_str();

    Stroka strokaObj = stdString;

    OutputMemo->Clear();
    OutputMemo->Lines->Add(strokaObj.GetStr());
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ATDtoCTDButtonClick(TObject *Sender)
{
    AnsiString inputStr = InputEdit->Text;

    Stroka strokaObj(inputStr.c_str());

    const char* stdString = strokaObj;

    OutputMemo->Clear();
    OutputMemo->Lines->Add(stdString);
}
//---------------------------------------------------------------------------
