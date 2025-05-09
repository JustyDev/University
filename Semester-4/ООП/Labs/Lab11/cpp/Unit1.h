//---------------------------------------------------------------------------

#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
#include <Vcl.Dialogs.hpp>
#include <Vcl.ExtCtrls.hpp>
#include <Vcl.Grids.hpp>
#include <Vcl.Mask.hpp>
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:	// IDE-managed Components
	TGroupBox *GroupBox1;
	TGroupBox *GroupBox2;
	TStringGrid *StringGrid1;
	TButton *Button1;
	TButton *Button2;
	TButton *Button3;
	TButton *Button4;
	TButton *Button5;
	TOpenDialog *OpenDialog1;
	TSaveDialog *SaveDialog1;
	TLabeledEdit *LabeledEdit1;
	TLabeledEdit *LabeledEdit2;
	TLabeledEdit *LabeledEdit3;
	TLabeledEdit *LabeledEdit4;
	TLabeledEdit *LabeledEdit5;
	TLabeledEdit *LabeledEdit6;
	TLabeledEdit *LabeledEdit7;
	TLabeledEdit *LabeledEdit8;
	TButton *Button6;
	TButton *Button7;
	TButton *Button8;
	TEdit *Edit1;
	void __fastcall Button1Click(TObject *Sender);
	void __fastcall Button2Click(TObject *Sender);
	void __fastcall Button3Click(TObject *Sender);
	void __fastcall FormCreate(TObject *Sender);
	void __fastcall Button4Click(TObject *Sender);
	void __fastcall Button5Click(TObject *Sender);
	void __fastcall Button6Click(TObject *Sender);
	void __fastcall FormClose(TObject *Sender, TCloseAction &Action);
	void __fastcall Button7Click(TObject *Sender);
	void __fastcall Button8Click(TObject *Sender);
private:	// User declarations
public:		// User declarations
	__fastcall TForm1(TComponent* Owner);
};

class Tovar {
	private:
		String name;
		int number;
		float price;
	public:
		Tovar() : name(""), number(0), price(0) {};
        virtual ~Tovar() {};
		virtual void add_rec(int flag);

		virtual void show(int rowIndex);

		virtual void clear(int flag);

		virtual void add_grid(const String& nameStr, const String& numberStr, const String& priceStr);

		float get_price();
};

class TovarProm : public Tovar {
	public:
		void add_rec();

        void clear();
};

class TovarProd : public Tovar {
	private:
		int term;
		int temp;
	public:
		void add_rec();

		void show(int rowIndex);

		void clear();

		void add_grid(const String& nameStr, const String& numberStr, const String& priceStr, const String& termStr, const String& tempStr);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
