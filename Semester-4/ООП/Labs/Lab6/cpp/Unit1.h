
//---------------------------------------------------------------------------
#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
#include "Unit2.h"
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published: // IDE-managed Components
    TEdit *InputEdit;
    TButton *CTDtoATDButton;
    TButton *ATDtoCTDButton;
    TMemo *OutputMemo;
    TLabel *Label1;
    void __fastcall CTDtoATDButtonClick(TObject *Sender);
    void __fastcall ATDtoCTDButtonClick(TObject *Sender);
private: // User declarations
public:  // User declarations
    __fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif

