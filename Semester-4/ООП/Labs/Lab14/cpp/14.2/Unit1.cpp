//---------------------------------------------------------------------------

#include <vcl.h>
#include <vector>
#include <algorithm>
#include <queue>
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
void __fastcall TForm1::FormCreate(TObject *Sender)
{
    StringGrid1->ColCount = 5;
	StringGrid1->RowCount = 1;

	StringGrid1->Cells[0][0] = L"Рейс";
	StringGrid1->Cells[1][0] = L"Тип самолета";
	StringGrid1->Cells[2][0] = L"Кол-во билетов";
	StringGrid1->Cells[3][0] = L"Цена";
    StringGrid1->Cells[4][0] = L"Дата вылета";

	for (int col = 0; col < StringGrid1->ColCount; ++col) {
        int maxWidth = StringGrid1->Canvas->TextWidth(StringGrid1->Cells[col][0]) + 20;
        StringGrid1->ColWidths[col] = maxWidth;
	}

	SaveDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
	OpenDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonAddClick(TObject *Sender)
{
    try {
		Reis r(
		LE_Reis->Text,
		LE_Type->Text,
		StrToInt(LE_Kol->Text),
		StrToFloat(LE_Price->Text),
		DateTimePicker1->Date
		);

		Reis::AddToGrid(StringGrid1, r);

        flightQueue.Enqueue(r);
    } catch (...) {
        ShowMessage(L"Ошибка ввода данных!");
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
void Reis::AddToGrid(TStringGrid *grid, const Reis &r)
{
    int row = grid->RowCount;
	grid->RowCount = row + 1;

    grid->Cells[0][row] = r.name;
    grid->Cells[1][row] = r.type;
    grid->Cells[2][row] = IntToStr(r.kol);
	grid->Cells[3][row] = FloatToStrF(r.price, ffFixed, 8, 2);
    grid->Cells[4][row] = FormatDateTime("dd.mm.yyyy", r.date);

    for (int col = 0; col < grid->ColCount; ++col) {
        int textWidth = grid->Canvas->TextWidth(grid->Cells[col][row]) + 20;
        if (textWidth > grid->ColWidths[col])
            grid->ColWidths[col] = textWidth;
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
					  grid->Cells[3][i] + "," +
					  grid->Cells[4][i];
        list->Add(line);
    }

    list->SaveToFile(filename, TEncoding::UTF8);
    delete list;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonLoadClick(TObject *Sender)
{
    if (OpenDialog1->Execute()) {
        Reis::LoadFromFile(StringGrid1, OpenDialog1->FileName, flightQueue);
    }
}
//---------------------------------------------------------------------------
void Reis::LoadFromFile(TStringGrid *grid, String filename, FlightQueue& queue)
{
    TStringList *list = new TStringList();
    list->LoadFromFile(filename, TEncoding::UTF8);

    // Очищаем grid и очередь перед загрузкой
    grid->RowCount = 1;
    while (!queue.IsEmpty()) {
        queue.Dequeue();
    }

    for (int i = 0; i < list->Count; ++i) {
        TStringList *cols = new TStringList();
        cols->StrictDelimiter = true;
        cols->Delimiter = ',';
        cols->DelimitedText = list->Strings[i];

        if (cols->Count >= 5) {
            try {
                TDate flightDate = StrToDate(cols->Strings[4]);
                Reis r(
                    cols->Strings[0],
                    cols->Strings[1],
                    StrToInt(cols->Strings[2]),
                    StrToFloat(cols->Strings[3]),
                    flightDate
                );

                AddToGrid(grid, r);
                queue.Enqueue(r);
            }
			catch (...) {

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
void Reis::SortByName(TStringGrid *grid)
{
    int rowCount = grid->RowCount;
    std::vector<Reis> data;

    for (int i = 1; i < rowCount; i++) {
        TDate flightDate = StrToDate(grid->Cells[4][i]);

        data.emplace_back(
            grid->Cells[0][i],
			grid->Cells[1][i],
			StrToInt(grid->Cells[2][i]),
			StrToFloat(grid->Cells[3][i]),
			flightDate
        );
    }

    std::sort(data.begin(), data.end(), [](const Reis &a, const Reis &b) {
        return a.name < b.name;
    });

    grid->RowCount = 1;
    for (const auto &r : data)
        AddToGrid(grid, r);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonSortByPriceClick(TObject *Sender)
{
    Reis::SortByPrice(StringGrid1);
}
//---------------------------------------------------------------------------
void Reis::SortByPrice(TStringGrid *grid)
{
    int rowCount = grid->RowCount;
    std::vector<Reis> data;

    for (int i = 1; i < rowCount; i++) {
        TDate flightDate = StrToDate(grid->Cells[4][i]);

        data.emplace_back(
            grid->Cells[0][i],
            grid->Cells[1][i],
            StrToInt(grid->Cells[2][i]),
            StrToFloat(grid->Cells[3][i]),
            flightDate
        );
    }

    std::sort(data.begin(), data.end(), [](const Reis &a, const Reis &b) {
        return a.price < b.price;
    });

    grid->RowCount = 1;
    for (const auto &r : data)
        AddToGrid(grid, r);
}
void __fastcall TForm1::ButtonDepartureClick(TObject *Sender)
{
    if (flightQueue.IsEmpty()) {
        ShowMessage(L"Очередь вылетов пуста!");
        return;
    }

    TForm* queueForm = new TForm(this);
    queueForm->Caption = L"Очередь вылетов (отсортировано по дате)";
    queueForm->Width = 850;
    queueForm->Height = 400;

    TStringGrid* queueGrid = new TStringGrid(queueForm);
    queueGrid->Parent = queueForm;
    queueGrid->Align = alClient;
    queueGrid->ScrollBars = ssBoth;
    queueGrid->Options << goColSizing << goRowSelect;

    queueGrid->ColCount = 5;
    queueGrid->Cells[0][0] = L"Рейс";
    queueGrid->Cells[1][0] = L"Тип самолета";
    queueGrid->Cells[2][0] = L"Кол-во билетов";
    queueGrid->Cells[3][0] = L"Цена";
    queueGrid->Cells[4][0] = L"Дата вылета";

	flightQueue.DisplayQueue(queueGrid, true);

    for (int col = 0; col < queueGrid->ColCount; col++) {
        int maxWidth = queueGrid->Canvas->TextWidth(queueGrid->Cells[col][0]) + 20;
        for (int row = 1; row < queueGrid->RowCount; row++) {
            int textWidth = queueGrid->Canvas->TextWidth(queueGrid->Cells[col][row]) + 20;
            if (textWidth > maxWidth) {
                maxWidth = textWidth;
            }
        }
        queueGrid->ColWidths[col] = maxWidth;
    }

    queueForm->ShowModal();
    delete queueForm;
}
//---------------------------------------------------------------------------
