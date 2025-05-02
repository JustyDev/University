//---------------------------------------------------------------------------

#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
#include <Vcl.ComCtrls.hpp>
#include <Vcl.Dialogs.hpp>
#include <Vcl.ExtCtrls.hpp>
#include <Vcl.Samples.Spin.hpp>
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:    // IDE-managed Components
    TImage *Image1;
    TButton *Button1;
    TButton *Button2;
    TButton *Button3;
    TButton *Button4;
    TButton *Button5;
    TButton *Button6;
    TStatusBar *StatusBar1;
    TSpinEdit *SpinEdit1;
    TSpinEdit *SpinEdit2;
    TLabel *Label1;
    TLabel *Label2;
    TRadioGroup *RadioGroup1;
    TRadioGroup *RadioGroup2;
    TOpenDialog *OpenDialog1;
    TSaveDialog *SaveDialog1;
    void __fastcall Image1MouseDown(TObject *Sender, TMouseButton Button, TShiftState Shift,
          int X, int Y);
    void __fastcall Image1MouseMove(TObject *Sender, TShiftState Shift, int X, int Y);
    void __fastcall FormCreate(TObject *Sender);
    void __fastcall Button1Click(TObject *Sender);
    void __fastcall Button2Click(TObject *Sender);
    void __fastcall Button3Click(TObject *Sender);
    void __fastcall Image1MouseUp(TObject *Sender, TMouseButton Button, TShiftState Shift,
          int X, int Y);

private:    // User declarations
public:        // User declarations
    __fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------

struct Figura{
        int x1;
        int y1;
        int x2;
        int y2;
        AnsiString Cvet;
        AnsiString TipFigury;
};

extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
