//---------------------------------------------------------------------------

#include <vcl.h>
#include <vector>
#pragma hdrstop

#include "Unit1.h"
#include "Unit2.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;
std::vector<train> trains;
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
	Form1->StringGrid1->ColCount = 4;

	Form1->StringGrid1->Cells[0][0] = L"Дата";
	StringGrid1->ColWidths[0] = 140;
	Form1->StringGrid1->Cells[1][0] = L"Время";
	StringGrid1->ColWidths[1] = 140;
	Form1->StringGrid1->Cells[2][0] = L"Место назначения";
	StringGrid1->ColWidths[2] = 200;
    Form1->StringGrid1->Cells[3][0] = L"Свободных мест";
	StringGrid1->ColWidths[3] = 130;

    SaveDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
	OpenDialog1->Filter = L"Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*";
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	train tr(Form1->datetrain->Date, Form1->timetrain->Time, Form1->Edit1->Text, StrToInt(Form1->Edit2->Text));
    trains.push_back(tr);
    StringGrid1->RowCount = 0;
	int row_count = StringGrid1->RowCount;

    for (int i = 0; i < trains.size(); i++,row_count++) {

        StringGrid1->RowCount = row_count + 1;
		Form1->StringGrid1->Cells[0][row_count] = trains[i].get_date();
		Form1->StringGrid1->Cells[1][row_count] = trains[i].get_time();
        Form1->StringGrid1->Cells[2][row_count] =
			trains[i].get_point();
        Form1->StringGrid1->Cells[3][row_count] =
			IntToStr(trains[i].get_space());
    }
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button2Click(TObject *Sender)
{
    bool good = false;
    StringGrid1->RowCount = 1;

    for (int i = 0; i < trains.size(); i++) {

        String sdate = Form1->datetrain->Date;
        if(sdate !=  trains[i].get_date())
        continue;

		if (Form1->Edit1->Text != "" && Form1->Edit1->Text != trains[i].get_point())
		continue;

		String stime = Form1->timetrain->Time;
		if (stime < trains[i].get_time())
		continue;

        if (StrToInt(Form1->Edit2->Text) > trains[i].get_space())
        continue;

        good = true;
        int row_count = StringGrid1->RowCount;
        StringGrid1->RowCount = row_count + 1;
		Form1->StringGrid1->Cells[0][row_count] = trains[i].get_date();
		Form1->StringGrid1->Cells[1][row_count] = trains[i].get_time();
        Form1->StringGrid1->Cells[2][row_count] =
			trains[i].get_point();
		Form1->StringGrid1->Cells[3][row_count] =
			IntToStr(trains[i].get_space());
	}

    if (good == false)
        Application->MessageBox(L"Подходящих поездов нет", L"Внимание",
        MB_OKCANCEL);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button3Click(TObject *Sender)
{
    StringGrid1->RowCount = 1;

    for (int i = 0; i < trains.size(); i++) {

        int row_count = StringGrid1->RowCount;
        StringGrid1->RowCount = row_count + 1;
		Form1->StringGrid1->Cells[0][row_count] = trains[i].get_date();
		Form1->StringGrid1->Cells[1][row_count] = trains[i].get_time();
		Form1->StringGrid1->Cells[2][row_count] =
			trains[i].get_point();
		Form1->StringGrid1->Cells[3][row_count] =
			IntToStr(trains[i].get_space());
	}
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button4Click(TObject *Sender)
{
    trains.clear();
    StringGrid1->RowCount = 1;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button5Click(TObject *Sender)
{
	if (SaveDialog1->Execute()) {
		TStringList* list = new TStringList();
		try {
			list->WriteBOM = true; // Добавляем BOM для UTF-8
			list->DefaultEncoding = TEncoding::UTF8;

			for (int i = 0; i < StringGrid1->RowCount; i++) {
				list->Add(StringGrid1->Rows[i]->DelimitedText);
			}

			list->SaveToFile(SaveDialog1->FileName, TEncoding::UTF8);
			ShowMessage(L"Файл успешно сохранён!");
		}
		__finally {
			delete list;
		}
	}
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button6Click(TObject *Sender)
{
    if (OpenDialog1->Execute()) {
        TStringList *fileLines = new TStringList();
        try {
            fileLines->LoadFromFile(OpenDialog1->FileName, TEncoding::UTF8);

			// Очищаем таблицу и список поездов
			StringGrid1->RowCount = 1;
            trains.clear();

			for (int i = 1; i < fileLines->Count; i++) {
                StringGrid1->RowCount = StringGrid1->RowCount + 1;
                int currentRow = StringGrid1->RowCount - 1;

                StringGrid1->Rows[currentRow]->DelimitedText = fileLines->Strings[i];

                train tr(
                    StringGrid1->Cells[0][currentRow],
                    StringGrid1->Cells[1][currentRow],
                    StringGrid1->Cells[2][currentRow],
                    StrToInt(StringGrid1->Cells[3][currentRow])
                );
                trains.push_back(tr);
            }

            ShowMessage(L"Файл успешно загружен!");
        }
        __finally {
            delete fileLines;
        }
	}
}
//---------------------------------------------------------------------------
