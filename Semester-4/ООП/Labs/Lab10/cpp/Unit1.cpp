//---------------------------------------------------------------------------

#include <vcl.h>
#include <fstream.h>
#include <System.StrUtils.hpp>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;

int ProductType = 0;
int i = 0, j = 0;


class Tovar {
	private:
		String name;
		int number;
		float price;
	public:
		Tovar() : name(""), number(0), price(0) {};
		virtual ~Tovar() {};
		void add_rec() {
			if(ProductType == 0) {
				name = Form1->LabeledEdit1->Text;
				number = StrToInt(Form1->LabeledEdit2->Text);
				price = StrToFloat(Form1->LabeledEdit3->Text);
			}
			if(ProductType == 1) {
				name = Form1->LabeledEdit6->Text;
				number = StrToInt(Form1->LabeledEdit7->Text);
				price = StrToFloat(Form1->LabeledEdit8->Text);
			}
		}

		void show() {
			Form1->StringGrid1->Cells[0][i+j] = name;
			Form1->StringGrid1->Cells[1][i+j] = number;
			Form1->StringGrid1->Cells[2][i+j] = price;
		}

		void clear() {
			if(ProductType == 0) {
				Form1->LabeledEdit1->Clear();
				Form1->LabeledEdit2->Clear();
				Form1->LabeledEdit3->Clear();
			}
			if(ProductType == 1) {
				Form1->LabeledEdit6->Clear();
				Form1->LabeledEdit7->Clear();
				Form1->LabeledEdit8->Clear();
			}
		}

		virtual void add_grid(const String& nameStr, const String& numberStr, const String& priceStr) {
			name = nameStr;
			number = StrToInt(numberStr);
			price = StrToFloat(priceStr);
		}

		float get_price() {
			return price;
		}

};

class TovarProm : public Tovar {};

class TovarProd : public Tovar {
	private:
		int term;
		int temp;
	public:
		void show() {
			Tovar::show();
			Form1->StringGrid1->Cells[3][i+j] = term;
			Form1->StringGrid1->Cells[4][i+j] = temp;
		}


		void add_rec() {
			Tovar::add_rec();
			term = StrToInt(Form1->LabeledEdit4->Text);
            temp = StrToInt(Form1->LabeledEdit5->Text);
		}

		void clear() {
			Tovar::clear();
			Form1->LabeledEdit4->Clear();
			Form1->LabeledEdit5->Clear();
		}

		void add_grid(const String& nameStr, const String& numberStr, const String& priceStr, const String& termStr, const String& tempStr) {
			Tovar::add_grid(nameStr, numberStr, priceStr);
			term = StrToInt(termStr);
			temp = StrToInt(tempStr);
		}
};

const int K = 100;
TovarProd prod[K];
TovarProm prom[K];

//---------------------------------------------------------------------------
void __fastcall TForm1::Button5Click(TObject *Sender)
{
	if(OpenDialog1->Execute())
	{
		String filename = OpenDialog1->FileName;
		TStringList *list = new TStringList();

		try
		{
            try {
				list->LoadFromFile(filename, TEncoding::UTF8);
			}
            catch (...) {
				list->LoadFromFile(filename, TEncoding::GetEncoding(1251));
			}

			StringGrid1->RowCount = (StringGrid1->FixedRows > 0) ? 1 : 0;
			i = 0; j = 0;

            for(int k = 0; k < list->Count; k++)
            {
                String line = list->Strings[k].Trim();
                if (line.IsEmpty()) continue;

                TStringList *parts = new TStringList();
                parts->Delimiter = L' ';
				parts->DelimitedText = line;

				if(parts->Count == 3 && j < K)
				{
                    prom[j].add_grid(parts->Strings[0], parts->Strings[1], parts->Strings[2]);
					prom[j].show();
					j++;
					StringGrid1->RowCount++;
				}
				else if(parts->Count == 5 && i < K)
				{
					prod[i].add_grid(parts->Strings[0], parts->Strings[1], parts->Strings[2],
								   parts->Strings[3], parts->Strings[4]);
					prod[i].show();
					i++;
					StringGrid1->RowCount++;
                }

                delete parts;
			}
		}
        __finally
		{
			delete list;
        }
	}
}
//---------------------------------------------------------------------------



//---------------------------------------------------------------------------
void __fastcall TForm1::Button2Click(TObject *Sender)
{
	ProductType = 1;
	prom[j].add_rec();
	prom[j].show();
	j++;
	prom[j].clear();
	StringGrid1->RowCount++;
}

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	ProductType = 0;
	prod[i].add_rec();
	prod[i].show();
	i++;
	prod[i].clear();
    StringGrid1->RowCount++;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button3Click(TObject *Sender)
{
	if(i == 0 && j == 0) {
		ShowMessage(L"Нет товаров!");
	} else {
		float sum = 0.0;
		for (int e = 0; e < i; e++) {
			sum += prod[e].get_price();
		}
		for (int e = 0; e < j; e++) {
            sum += prom[e].get_price();
		}
		ShowMessage(L"Общая стоимость: " + FloatToStr(sum));
    }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::FormCreate(TObject *Sender)
{
	StringGrid1->FixedCols = 0;
	StringGrid1->FixedRows = 0;

	StringGrid1->ColCount = 5;
	StringGrid1->RowCount = 0;
	StringGrid1->ColWidths[0] = 150;
	StringGrid1->ColWidths[1] = 110;

    SaveDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
	OpenDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button4Click(TObject *Sender)
{
	if(SaveDialog1->Execute())
    {
        String filename = SaveDialog1->FileName;
        TStringList *list = new TStringList();

        for (int i = 0; i < StringGrid1->RowCount; i++)
        {
			StringGrid1->Rows[i]->Delimiter = L' ';
			String line = StringGrid1->Rows[i]->DelimitedText;
			list->Add(line);
		}

        list->SaveToFile(filename, TEncoding::UTF8);
        delete list;
	}
}
