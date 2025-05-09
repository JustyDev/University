//---------------------------------------------------------------------------

#include <vcl.h>
#include <fstream>
#include <vector>
#include <algorithm>
#include <System.StrUtils.hpp>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;

std::vector<Tovar*> allTovars;
const int MAX = 200;

void Tovar::add_rec(int flag) {
	if(flag == 0) {
		name = Form1->LabeledEdit1->Text;
		number = StrToInt(Form1->LabeledEdit2->Text);
		price = StrToFloat(Form1->LabeledEdit3->Text);
	}
	if(flag == 1) {
		name = Form1->LabeledEdit6->Text;
		number = StrToInt(Form1->LabeledEdit7->Text);
		price = StrToFloat(Form1->LabeledEdit8->Text);
	}
}

void Tovar::show(int rowIndex) {
    Form1->StringGrid1->Cells[0][rowIndex] = name;
    Form1->StringGrid1->Cells[1][rowIndex] = number;
    Form1->StringGrid1->Cells[2][rowIndex] = price;
}

void Tovar::clear(int flag) {
	if(flag == 0) {
		Form1->LabeledEdit1->Clear();
		Form1->LabeledEdit2->Clear();
		Form1->LabeledEdit3->Clear();
	}
	if(flag == 1) {
		Form1->LabeledEdit6->Clear();
		Form1->LabeledEdit7->Clear();
		Form1->LabeledEdit8->Clear();
	}
}

void Tovar::add_grid(const String& nameStr, const String& numberStr, const String& priceStr) {
	name = nameStr;
	number = StrToInt(numberStr);
	price = StrToFloat(priceStr);
}

float Tovar::get_price() {
	return price;
}

//---------------------------------------------------------------------------
void TovarProm::add_rec() {
    Tovar::add_rec(1);
}

void TovarProm::clear() {
	Tovar::clear(1);
}


void TovarProd::add_rec() {
	Tovar::add_rec(0);
	term = StrToInt(Form1->LabeledEdit4->Text);
	temp = StrToInt(Form1->LabeledEdit5->Text);
}

void TovarProd::show(int rowIndex) {
    Tovar::show(rowIndex);
    Form1->StringGrid1->Cells[3][rowIndex] = term;
    Form1->StringGrid1->Cells[4][rowIndex] = temp;
}

void TovarProd::clear() {
	Tovar::clear(0);
	Form1->LabeledEdit4->Clear();
	Form1->LabeledEdit5->Clear();
}

void TovarProd::add_grid(const String& nameStr, const String& numberStr, const String& priceStr, const String& termStr, const String& tempStr) {
	Tovar::add_grid(nameStr, numberStr, priceStr);
	term = StrToInt(termStr);
	temp = StrToInt(tempStr);
}

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
}
//---------------------------------------------------------------------------
void UpdateGrid(){
	Form1->StringGrid1->RowCount = allTovars.size();

    for (size_t i = 0; i < allTovars.size(); i++) {
        if (dynamic_cast<TovarProd*>(allTovars[i])) {
            dynamic_cast<TovarProd*>(allTovars[i])->show(i);
        } else {
            dynamic_cast<TovarProm*>(allTovars[i])->show(i);
        }
    }
    Form1->StringGrid1->Repaint();
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	if (allTovars.size() >= MAX) {
        ShowMessage(L"Достигнуто максимальное количество товаров!");
        return;
    }

    TovarProd* prod = new TovarProd;
    prod->add_rec();
    allTovars.push_back(prod);

    UpdateGrid();
    prod->clear();
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button2Click(TObject *Sender)
{
    if (allTovars.size() >= MAX) {
        ShowMessage(L"Достигнуто максимальное количество товаров!");
        return;
    }

    TovarProm* prom = new TovarProm;
    prom->add_rec();
    allTovars.push_back(prom);

    UpdateGrid();
    prom->clear();
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button3Click(TObject *Sender)
{
	if(allTovars.empty()) {
		ShowMessage(L"Нет товаров!");
	} else {
		float sum = 0.0;
		for (unsigned int e = 0; e < allTovars.size(); e++) {
			sum += allTovars[e]->get_price();
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

    StringGrid1->Options << goRowSelect << goAlwaysShowEditor;

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
			int i = 0;

            for(int k = 0; k < list->Count; k++)
            {
                String line = list->Strings[k].Trim();
                if (line.IsEmpty()) continue;

                TStringList *parts = new TStringList();
                parts->Delimiter = L' ';
				parts->DelimitedText = line;

				if(parts->Count == 3 && i < MAX)
				{
					TovarProm* prom = new TovarProm;
					prom->add_grid(parts->Strings[0], parts->Strings[1], parts->Strings[2]);
					prom->show(i);
                    i++;
					allTovars.push_back(prom);
					StringGrid1->RowCount++;
				}
				else if(parts->Count == 5 && i < MAX)
				{
                    TovarProd* prod = new TovarProd;
					prod->add_grid(parts->Strings[0], parts->Strings[1], parts->Strings[2],
								   parts->Strings[3], parts->Strings[4]);
					prod->show(i);
                    i++;
                    allTovars.push_back(prod);
					StringGrid1->RowCount++;
				}

                delete parts;
			}
            UpdateGrid();
        }
        __finally
        {
            delete list;
        }
    }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button6Click(TObject *Sender)
{
	if (StringGrid1->RowCount <= 0)
    {
        ShowMessage(L"Нет данных для сортировки!");
        return;
    }

    std::vector<TStringList*> gridData;
    for (int i = 0; i < StringGrid1->RowCount; i++)
    {
        TStringList* row = new TStringList();
        for (int j = 0; j < StringGrid1->ColCount; j++)
        {
            row->Add(StringGrid1->Cells[j][i]);
        }
        gridData.push_back(row);
    }

    for (size_t i = 0; i < gridData.size() - 1; i++)
    {
        for (size_t j = 0; j < gridData.size() - i - 1; j++)
        {
            if (gridData[j]->Strings[0] > gridData[j+1]->Strings[0])
            {
                std::swap(gridData[j], gridData[j+1]);
            }
        }
    }

    StringGrid1->RowCount = 0;
    StringGrid1->RowCount = gridData.size();

    for (int i = 0; i < (int)gridData.size(); i++)
    {
        for (int j = 0; j < gridData[i]->Count && j < StringGrid1->ColCount; j++)
        {
            StringGrid1->Cells[j][i] = gridData[i]->Strings[j];
        }
        delete gridData[i];
    }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::FormClose(TObject *Sender, TCloseAction &Action)
{
    for (std::vector<Tovar*>::iterator it = allTovars.begin(); it != allTovars.end(); ++it)
    {
        delete *it;
    }
    allTovars.clear();
}
//---------------------------------------------------------------------------

void __fastcall TForm1::Button7Click(TObject *Sender)
{
    if (StringGrid1->RowCount <= 0)
    {
        ShowMessage(L"Нет данных для сортировки!");
        return;
    }

    std::vector<TStringList*> gridData;
    for (int i = 0; i < StringGrid1->RowCount; i++)
    {
        TStringList* row = new TStringList();
        for (int j = 0; j < StringGrid1->ColCount; j++)
        {
            row->Add(StringGrid1->Cells[j][i]);
        }
        gridData.push_back(row);
    }

    for (size_t i = 0; i < gridData.size() - 1; i++)
    {
        for (size_t j = 0; j < gridData.size() - i - 1; j++)
		{
            float price1 = StrToFloatDef(gridData[j]->Strings[2], 0.0f);
            float price2 = StrToFloatDef(gridData[j+1]->Strings[2], 0.0f);

            if (price1 > price2)
            {
                std::swap(gridData[j], gridData[j+1]);
            }
        }
    }

    StringGrid1->RowCount = 0;
    StringGrid1->RowCount = gridData.size();

    for (int i = 0; i < (int)gridData.size(); i++)
    {
        for (int j = 0; j < gridData[i]->Count && j < StringGrid1->ColCount; j++)
        {
            StringGrid1->Cells[j][i] = gridData[i]->Strings[j];
        }
        delete gridData[i];
    }
}
//---------------------------------------------------------------------------

void __fastcall TForm1::Button8Click(TObject *Sender)
{
    if (StringGrid1->RowCount <= 0)
    {
        ShowMessage(L"Таблица пуста! Нет данных для поиска.");
        return;
    }

    UnicodeString searchText = Edit1->Text.Trim();
    if (searchText.IsEmpty())
    {
        ShowMessage(L"Введите текст для поиска в поле Edit1!");
        return;
    }

    bool found = false;
    UnicodeString results = L"Результаты поиска '" + searchText + L"':\n\n";

	// Поиск по всем ячейкам
    for (int row = 0; row < StringGrid1->RowCount; row++)
    {
        bool rowFound = false;
        UnicodeString rowData;

        for (int col = 0; col < StringGrid1->ColCount; col++)
        {
            if (StringGrid1->Cells[col][row].Pos(searchText) > 0)
            {
                if (!rowFound)
                {
                    rowData = L"Строка " + IntToStr(row + 1) + L": ";
                    rowFound = true;
                    found = true;
                }
                rowData += StringGrid1->Cells[col][row];
            }
        }

        if (rowFound)
        {
            results += rowData + L"\n";
        }
    }

    if (found)
    {
        ShowMessage(results);
    }
    else
    {
        ShowMessage(L"Значение '" + searchText + L"' не найдено в таблице.");
	}
}
//---------------------------------------------------------------------------

