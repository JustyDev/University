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
#include <vector>

class Reis {
public:
	String name;
	String type;
	int kol;
	float price;

	Reis(String n, String t, int k, float p)
		: name(n), type(t), kol(k), price(p) {}

	static void SortByName(TStringGrid *grid);
	static void SortByPrice(TStringGrid *grid);
	static void AddToGrid(TStringGrid *grid, const Reis &r);
	static void SaveToFile(TStringGrid *grid, String filename);
	static void LoadFromFile(TStringGrid *grid, String filename);
};
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:	// IDE-managed Components
	TStringGrid *StringGrid1;
	TButton *ButtonAdd;
	TButton *ButtonSave;
	TButton *ButtonLoad;
	TButton *ButtonSortByName;
	TButton *ButtonSortByPrice;
	TLabeledEdit *LE_Reis;
	TLabeledEdit *LE_Type;
	TLabeledEdit *LE_Kol;
	TLabeledEdit *LE_Price;
	TOpenDialog *OpenDialog1;
	TSaveDialog *SaveDialog1;
	void __fastcall ButtonLoadClick(TObject *Sender);
	void __fastcall ButtonSortByNameClick(TObject *Sender);
	void __fastcall ButtonSortByPriceClick(TObject *Sender);
	void __fastcall FormCreate(TObject *Sender);
	void __fastcall ButtonAddClick(TObject *Sender);
	void __fastcall ButtonSaveClick(TObject *Sender);
private:	// User declarations
public:		// User declarations
	__fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
