// Unit1.h

#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <Classes.hpp>
#include <Controls.hpp>
#include <StdCtrls.hpp>
#include <Forms.hpp>
#include <ExtCtrls.hpp>

#include <Windows.h>
#include <ctime>

//---------------------------------------------------------------------------
struct PInf {
    int Usage;
    int Threads;
    int PriClassBase;
    DWORD ID;
    DWORD V1, V2;
    HANDLE H;
    bool Suspended;
    FILETIME StartTime;
};

class TForm1 : public TForm
{
__published:	// IDE-managed Components
    TListBox *ListBox1;
    TButton *Button1;
    TButton *Button2;
    TTimer *Timer1;

    void __fastcall FormCreate(TObject *Sender);
    void __fastcall Timer1Timer(TObject *Sender);
    void __fastcall FormDestroy(TObject *Sender);
    void __fastcall Button1Click(TObject *Sender);
    void __fastcall Button2Click(TObject *Sender);

private:	// User declarations
    void __fastcall spisokprocessov();
    void __fastcall MTIcon(TMessage &a);
    BEGIN_MESSAGE_MAP
        MESSAGE_HANDLER(WM_USER + 1, TMessage, MTIcon)
    END_MESSAGE_MAP(TForm)
public:		// User declarations
    __fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
