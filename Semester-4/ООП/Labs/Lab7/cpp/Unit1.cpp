//---------------------------------------------------------------------------

#include <vcl.h>
#include <vector>
#include <algorithm>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonAddClick(TObject *Sender)
{
    try {
        Reis r(LE_Reis->Text, LE_Type->Text, StrToInt(LE_Kol->Text), StrToFloat(LE_Price->Text));
        Reis::AddToGrid(StringGrid1, r);
    } catch (...) {
        ShowMessage(L"Ошибка ввода данных!");
    }
}
//---------------------------------------------------------------------------
void Reis::AddToGrid(TStringGrid *grid, const Reis &r)
{
    int row = grid->RowCount;
	grid->RowCount = row + 1;

    grid->Cells[0][row] = r.name;
    grid->Cells[1][row] = r.type;
    grid->Cells[2][row] = IntToStr(r.kol);
	grid->Cells[3][row] = FloatToStrF(r.price, ffFixed, 8, 2);

    for (int col = 0; col < grid->ColCount; ++col) {
        int textWidth = grid->Canvas->TextWidth(grid->Cells[col][row]) + 20;
        if (textWidth > grid->ColWidths[col])
            grid->ColWidths[col] = textWidth;
    }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonSaveClick(TObject *Sender)
{
    if (SaveDialog1->Execute()) {
        Reis::SaveToFile(StringGrid1, SaveDialog1->FileName);
    }
}
//---------------------------------------------------------------------------
void Reis::SaveToFile(TStringGrid *grid, String filename)
{
    TStringList *list = new TStringList();

    for (int i = 1; i < grid->RowCount; i++) {
        String line = grid->Cells[0][i] + "," +
                      grid->Cells[1][i] + "," +
                      grid->Cells[2][i] + "," +
                      grid->Cells[3][i];
        list->Add(line);
    }

    list->SaveToFile(filename, TEncoding::UTF8);
    delete list;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonLoadClick(TObject *Sender)
{
    if (OpenDialog1->Execute()) {
        Reis::LoadFromFile(StringGrid1, OpenDialog1->FileName);
    }
}
//---------------------------------------------------------------------------
void Reis::LoadFromFile(TStringGrid *grid, String filename)
{
    TStringList *list = new TStringList();
    list->LoadFromFile(filename, TEncoding::UTF8);

    grid->RowCount = 1;

    for (int i = 0; i < list->Count; ++i) {
        TStringList *cols = new TStringList();
        cols->StrictDelimiter = true;
        cols->Delimiter = ',';
        cols->DelimitedText = list->Strings[i];

        if (cols->Count == 4) {
            try {
                Reis r(cols->Strings[0], cols->Strings[1],
                       StrToInt(cols->Strings[2]), StrToFloat(cols->Strings[3]));
                AddToGrid(grid, r);
            } catch (...) {
                // Пропустить строку с ошибкой
            }
        }

        delete cols;
    }

    delete list;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonSortByNameClick(TObject *Sender)
{
    Reis::SortByName(StringGrid1);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonSortByPriceClick(TObject *Sender)
{
    Reis::SortByPrice(StringGrid1);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::FormCreate(TObject *Sender)
{
	StringGrid1->ColCount = 4;
	StringGrid1->RowCount = 1;

	StringGrid1->Cells[0][0] = L"Рейс";
	StringGrid1->Cells[1][0] = L"Тип самолета";
	StringGrid1->Cells[2][0] = L"Кол-во билетов";
	StringGrid1->Cells[3][0] = L"Цена";

	for (int col = 0; col < StringGrid1->ColCount; ++col) {
		int maxWidth = StringGrid1->Canvas->TextWidth(StringGrid1->Cells[col][0]) + 20;
		StringGrid1->ColWidths[col] = maxWidth;
	}

	SaveDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
	OpenDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
}
//---------------------------------------------------------------------------
void Reis::SortByPrice(TStringGrid *grid)
{
    int rowCount = grid->RowCount;
    std::vector<Reis> data;
    for (int i = 1; i < rowCount; i++) {
        data.emplace_back(grid->Cells[0][i], grid->Cells[1][i],
                          StrToInt(grid->Cells[2][i]), StrToFloat(grid->Cells[3][i]));
    }
    std::sort(data.begin(), data.end(), [](const Reis &a, const Reis &b) {
        return a.price < b.price;
    });

    grid->RowCount = 1;
    for (const auto &r : data)
        AddToGrid(grid, r);
}
//---------------------------------------------------------------------------
void Reis::SortByName(TStringGrid *grid)
{
    int rowCount = grid->RowCount;
    std::vector<Reis> data;
    for (int i = 1; i < rowCount; i++) {
        data.emplace_back(grid->Cells[0][i], grid->Cells[1][i],
                          StrToInt(grid->Cells[2][i]), StrToFloat(grid->Cells[3][i]));
    }
    std::sort(data.begin(), data.end(), [](const Reis &a, const Reis &b) {
        return a.name < b.name;
    });

    grid->RowCount = 1;
    for (const auto &r : data)
        AddToGrid(grid, r);
}