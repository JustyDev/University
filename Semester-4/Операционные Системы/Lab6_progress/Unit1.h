// Включите в .h файл:
#include <vcl.h>
#include <System.hpp>
#include <IdSNTP.hpp>
#include <Windows.h>
#include <IdBaseComponent.hpp>
#include <IdComponent.hpp>
#include <IdTCPClient.hpp>
#include <IdTCPConnection.hpp>
#include <IdTime.hpp>
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.ExtCtrls.hpp>
#include <Vcl.Mask.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.ComCtrls.hpp>

// Объявление формы
class TForm1 : public TForm
{
__published:    // IDE-managed Components
    TButton *Button1;
    TButton *Button2;
	TIdTime *IdTime1;
    TLabeledEdit *LabeledEdit1;
    TLabeledEdit *LabeledEdit2;
    TLabeledEdit *LabeledEdit3;
    TTimer *Timer1;
	TRichEdit *RichEdit1;

    void __fastcall Button1Click(TObject *Sender);
	void __fastcall Button2Click(TObject *Sender);
    void __fastcall FormCreate(TObject *Sender);
    void __fastcall Timer1Timer(TObject *Sender);

private:    // User declarations
	void SetSystemTime(TDateTime DateTime);
	TDateTime ParseNistTimeResponse(const String &response);

public:        // User declarations
    __fastcall TForm1(TComponent* Owner);
};

