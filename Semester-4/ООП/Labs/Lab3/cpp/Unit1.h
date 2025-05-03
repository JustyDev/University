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
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:    // IDE-managed Components
    TMemo *Memo1;
    TButton *Button1;
    TLabeledEdit *LabeledEdit1;
    TLabeledEdit *LabeledEdit2;
	TButton *Button2;
	void __fastcall Button1Click(TObject *Sender);
	void __fastcall Button2Click(TObject *Sender);

private:    // User declarations
public:        // User declarations
    __fastcall TForm1(TComponent* Owner);
};

class MyTime {
 private:
    int chas;
    int min;
    int sec;
 public:
    MyTime() { chas=0; min=0; sec=0; }
	MyTime(int ch, int m, int s) {
	   chas=ch; min=m; sec=s;
    }
    void show();
    void summa(MyTime t1, MyTime t2);
    bool parseTimeString(const AnsiString &timeStr);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
