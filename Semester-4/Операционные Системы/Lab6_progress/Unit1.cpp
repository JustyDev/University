#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
#pragma package(smart_init)
#pragma resource "*.dfm"

TForm1 *Form1;

__fastcall TForm1::TForm1(TComponent* Owner)
    : TForm(Owner)
{
}

void __fastcall TForm1::FormCreate(TObject *Sender)
{
    // Настройка компонентов при создании формы
    LabeledEdit1->EditLabel->Caption = "Сервер синхронизации";
    LabeledEdit1->Text = "time.nist.gov";

    LabeledEdit2->EditLabel->Caption = "Дата";
    LabeledEdit2->ReadOnly = true;

    LabeledEdit3->EditLabel->Caption = "Время";
	LabeledEdit3->ReadOnly = true;

    Button1->Caption = "Получить время";
    Button2->Caption = "Синхронизировать";

    // Настраиваем таймер (отключен по умолчанию)
    Timer1->Enabled = false;
    Timer1->Interval = 1000; // 1 секунда

    // Настройка компонента IdTime1 как TIdTCPClient
    IdTime1->Host = LabeledEdit1->Text;
    IdTime1->Port = 13; // Порт для Daytime протокола
    IdTime1->ReadTimeout = 5000; // 5 секунд на чтение
    IdTime1->ConnectTimeout = 5000; // 5 секунд на подключение
}

void __fastcall TForm1::Button1Click(TObject *Sender)
{
    try
    {
        Screen->Cursor = crHourGlass;

        // Получаем хост из поля ввода
        IdTime1->Host = LabeledEdit1->Text;

		if (!IdTime1->Connected()) {
			IdTime1->Connect();
		}

		// Читаем ответ от сервера
		String response = IdTime1->IOHandler->ReadLn();
		IdTime1->Disconnect();

		RichEdit1->Text = response;

		// Парсим ответ сервера и получаем дату/время
		TDateTime serverTime = ParseNistTimeResponse(response);

		// Форматируем и отображаем дату и время
		LabeledEdit2->Text = serverTime.FormatString("yyyy-mm-dd");
		LabeledEdit3->Text = serverTime.FormatString("hh:nn:ss");

		Screen->Cursor = crDefault;
	}
	catch (Exception &e)
	{
		Screen->Cursor = crDefault;
		ShowMessage("Ошибка при получении времени: " + e.Message +
				   "\n\nПопробуйте другой сервер, например:\n- time.windows.com\n- pool.ntp.org\n- time.google.com");
	}
}

TDateTime TForm1::ParseNistTimeResponse(const String &response)
{
    // Формат ответа NIST: JJJJJ YY-MM-DD HH:MM:SS TT L H msADV UTC(NIST) *
    // Например: 60798 25-05-03 21:39:18 50 0 0 539.0 UTC(NIST) *

    try {
        // Выводим в лог для отладки
        // ShowMessage("Получен ответ от сервера: " + response);

        // Разбиваем строку на части по пробелу
        int spacePos1 = response.Pos(" ");
        if (spacePos1 <= 0) throw Exception("Некорректный формат ответа");

		int spacePos2 = response.Pos(" ", spacePos1 + 1);
        if (spacePos2 <= 0) throw Exception("Некорректный формат ответа");

        int spacePos3 = response.Pos(" ", spacePos2 + 1);
        if (spacePos3 <= 0) throw Exception("Некорректный формат ответа");

        // Извлекаем дату и время
        String dateStr = response.SubString(spacePos1 + 1, spacePos2 - spacePos1 - 1); // YY-MM-DD
        String timeStr = response.SubString(spacePos2 + 1, spacePos3 - spacePos2 - 1); // HH:MM:SS

        // Получаем компоненты даты
        int firstDash = dateStr.Pos("-");
        int secondDash = dateStr.Pos("-", firstDash + 1);

        if (firstDash <= 0 || secondDash <= 0)
            throw Exception("Некорректный формат даты");

        int yy = StrToIntDef(dateStr.SubString(1, firstDash - 1), 0);
        int mm = StrToIntDef(dateStr.SubString(firstDash + 1, secondDash - firstDash - 1), 0);
        int dd = StrToIntDef(dateStr.SubString(secondDash + 1, dateStr.Length() - secondDash), 0);

        // Преобразуем 2-цифровой год в 4-цифровой
        int fullYear = (yy < 70) ? 2000 + yy : 1900 + yy;

        // Получаем компоненты времени
        int firstColon = timeStr.Pos(":");
        int secondColon = timeStr.Pos(":", firstColon + 1);

        if (firstColon <= 0 || secondColon <= 0)
            throw Exception("Некорректный формат времени");

        int hh = StrToIntDef(timeStr.SubString(1, firstColon - 1), 0);
        int mn = StrToIntDef(timeStr.SubString(firstColon + 1, secondColon - firstColon - 1), 0);
        int ss = StrToIntDef(timeStr.SubString(secondColon + 1, timeStr.Length() - secondColon), 0);

        // Создаем TDateTime объект
        TDateTime result = EncodeDate(fullYear, mm, dd) + EncodeTime(hh, mn, ss, 0);

        return result;
    }
    catch (Exception &e)
    {
        throw Exception("Ошибка при разборе ответа от сервера: " + e.Message + "\nОтвет: " + response);
    }
}

void __fastcall TForm1::Button2Click(TObject *Sender)
{
	try
	{
		// Проверяем, что поля не пустые
		if (LabeledEdit2->Text.IsEmpty() || LabeledEdit3->Text.IsEmpty())
		{
			ShowMessage("Сначала получите время с сервера!");
            return;
        }

        // Парсим дату и время в TDateTime объект
        TDateTime dateTime;
        try
        {
            String dateTimeStr = LabeledEdit2->Text + " " + LabeledEdit3->Text;
            dateTime = StrToDateTime(dateTimeStr);
        }
        catch (...)
        {
            ShowMessage("Неверный формат даты или времени!");
            return;
        }

        // Устанавливаем системное время
        SetSystemTime(dateTime);

        ShowMessage("Время успешно синхронизировано!");
    }
    catch (Exception &e)
    {
        ShowMessage("Ошибка при синхронизации времени: " + e.Message);
    }
}

void __fastcall TForm1::Timer1Timer(TObject *Sender)
{
    // Функционал таймера если нужно
}

void TForm1::SetSystemTime(TDateTime DateTime)
{
    // Преобразуем TDateTime в структуру SYSTEMTIME
    SYSTEMTIME st;
    Word year, month, day, hour, min, sec, msec;

    DateTime.DecodeDate(&year, &month, &day);
    DateTime.DecodeTime(&hour, &min, &sec, &msec);

    st.wYear = year;
    st.wMonth = month;
    st.wDay = day;
    st.wHour = hour;
    st.wMinute = min;
    st.wSecond = sec;
    st.wMilliseconds = msec;

    // Для установки системного времени нужны права администратора
    if (!SetLocalTime(&st))
    {
        int error = GetLastError();
        throw Exception("Не удалось установить системное время. Код ошибки: " + IntToStr(error) +
                       "\nВозможно, нужны права администратора.");
    }
}
