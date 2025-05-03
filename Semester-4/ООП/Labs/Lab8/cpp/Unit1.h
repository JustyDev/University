
//---------------------------------------------------------------------------
#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
#include <Vcl.ExtCtrls.hpp>
#include <Vcl.Mask.hpp>
#include "Unit2.h"
//---------------------------------------------------------------------------

class FloatPr : public Float {
  public:
     FloatPr();
     FloatPr(float v);
     FloatPr(Float a);
     FloatPr operator-(FloatPr b);
     FloatPr operator*(FloatPr b);
     FloatPr operator/(FloatPr b);
};

class TForm1 : public TForm
{
__published:
  TButton *Button1;
  TButton *Button2;
  TButton *Button3;
  TButton *Button4;
  TLabeledEdit *LabeledEdit1;
  TLabeledEdit *LabeledEdit2;
  TPanel *Panel1;
  void __fastcall Button1Click(TObject *Sender);
  void __fastcall Button2Click(TObject *Sender);
  void __fastcall Button3Click(TObject *Sender);
  void __fastcall Button4Click(TObject *Sender);

private:  // User declarations
  bool ValidateInput();

public:    // User declarations
  __fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif

