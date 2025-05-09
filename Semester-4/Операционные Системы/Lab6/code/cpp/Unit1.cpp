//---------------------------------------------------------------------------

#include <vcl.h>
#include <IdTime.hpp>
#include <SysUtils.hpp>
#include <DateUtils.hpp>
#include <windows.h>
#include <math.h>
#pragma hdrstop

#include "Unit1.h"
#ifdef __cplusplus
int min (int value1, int value2);

   int min(int value1, int value2)
   {
      return ( (value1 < value2) ? value1 : value2);
   }

#endif
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
void __fastcall TForm1::btnConnectClick(TObject *Sender)
{
	try {
		IdTime1->Host = editNTP->Text;
        TDateTime currentTime = IdTime1->DateTime;

		editDate->Text = DateToStr(currentTime);
        editTime->Text = TimeToStr(currentTime);

        IdTime1->Disconnect();
	} catch (Exception &e) {
		ShowMessage(L"Ошибка поключения: " + e.Message);
	}
}
//---------------------------------------------------------------------------
void __fastcall TForm1::btnSynchronizeClick(TObject *Sender)
{
	try {
		SYSTEMTIME st;

		TDateTime localTime = StrToDateTime(editDate->Text + " " + editTime->Text);
        TDateTime utcTime = TTimeZone::Local->ToUniversalTime(localTime);

		unsigned short year, month, day;
		utcTime.DecodeDate(&year, &month, &day);

		unsigned short hour, minute, second, msec;
		utcTime.DecodeTime(&hour, &minute, &second, &msec);

		st.wYear = year;
        st.wMonth = month;
        st.wDay = day;
        st.wHour = hour;
        st.wMinute = minute;
        st.wSecond = second;
		st.wMilliseconds = 0;

		if (SetSystemTime(&st)) {
            ShowMessage(L"Точные дата и время синхронизированы.");
		} else {
			DWORD err = GetLastError();
			ShowMessage(L"Ошибка при синхронизации времени." + String(err));
        }
	} catch (Exception &e) {
        ShowMessage(L"Ошибка синхронизации: " + e.Message);
	}
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Timer1Timer(TObject *Sender)
{
    TCanvas *Canvas = Image1->Canvas;

	int w = Image1->Width;
	int h = Image1->Height;
	int centerX = w / 2;
	int centerY = h / 2;
	int radius = min(w, h) / 2 - 10;

	TDateTime currentTime = Now();
	Word hour, minute, second, millisecond;
	DecodeTime(currentTime, hour, minute, second, millisecond);

	int hours = hour % 12;
	int minutes = minute;
	int seconds = second;

	Canvas->Brush->Color = Form1->Color;
	Canvas->FillRect(Rect(0, 0, w, h));

	Canvas->Pen->Color = clBlack;
	Canvas->Brush->Color = (TColor)RGB(213, 245, 228);
	Canvas->Ellipse(centerX - radius, centerY - radius, centerX + radius, centerY + radius);

	//Засечки
	for (int i = 0; i < 60; ++i) {
		double angle = i * 6.0 * M_PI / 180.0;
		int outerX = centerX + radius * cos(angle - M_PI_2);
		int outerY = centerY + radius * sin(angle - M_PI_2);

        int innerRadius = (i % 5 == 0) ? radius - 10 : radius - 5;
		int innerX = centerX + innerRadius * cos(angle - M_PI_2);
		int innerY = centerY + innerRadius * sin(angle - M_PI_2);

		Canvas->Pen->Width = (i % 5 == 0) ? 2 : 1;
		Canvas->Pen->Color = clBlack;
		Canvas->MoveTo(outerX, outerY);
        Canvas->LineTo(innerX, innerY);
	}

	// Углы для стрелок
	double angleHour = (hours + minutes / 60.0) * 30.0 * M_PI / 180.0;
	double angleMinute = minutes * 6.0 * M_PI / 180.0;
	double angleSecond = seconds * 6.0 * M_PI / 180.0;

	// Стрелка часов
	Canvas->Pen->Color = clBlack;
	Canvas->Pen->Width = 4;
	Canvas->MoveTo(centerX, centerY);
	Canvas->LineTo(centerX + radius * 0.5 * cos(angleHour - M_PI_2),
				   centerY + radius * 0.5 * sin(angleHour - M_PI_2));

	// Стрелка минут
	Canvas->Pen->Color = clBlue;
	Canvas->Pen->Width = 3;
	Canvas->MoveTo(centerX, centerY);
	Canvas->LineTo(centerX + radius * 0.7 * cos(angleMinute - M_PI_2),
				   centerY + radius * 0.7 * sin(angleMinute - M_PI_2));

	// Стрелка секунд
	Canvas->Pen->Color = clRed;
	Canvas->Pen->Width = 1;
	Canvas->MoveTo(centerX, centerY);
	Canvas->LineTo(centerX + radius * 0.9 * cos(angleSecond - M_PI_2),
				   centerY + radius * 0.9 * sin(angleSecond - M_PI_2));
}
//---------------------------------------------------------------------------
