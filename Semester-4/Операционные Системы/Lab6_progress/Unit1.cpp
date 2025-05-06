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
    // ��������� ����������� ��� �������� �����
    LabeledEdit1->EditLabel->Caption = "������ �������������";
    LabeledEdit1->Text = "time.nist.gov";

    LabeledEdit2->EditLabel->Caption = "����";
    LabeledEdit2->ReadOnly = true;

    LabeledEdit3->EditLabel->Caption = "�����";
	LabeledEdit3->ReadOnly = true;

    Button1->Caption = "�������� �����";
    Button2->Caption = "����������������";

    // ����������� ������ (�������� �� ���������)
    Timer1->Enabled = false;
    Timer1->Interval = 1000; // 1 �������

    // ��������� ���������� IdTime1 ��� TIdTCPClient
    IdTime1->Host = LabeledEdit1->Text;
    IdTime1->Port = 13; // ���� ��� Daytime ���������
    IdTime1->ReadTimeout = 5000; // 5 ������ �� ������
    IdTime1->ConnectTimeout = 5000; // 5 ������ �� �����������
}

void __fastcall TForm1::Button1Click(TObject *Sender)
{
    try
    {
        Screen->Cursor = crHourGlass;

        // �������� ���� �� ���� �����
        IdTime1->Host = LabeledEdit1->Text;

		if (!IdTime1->Connected()) {
			IdTime1->Connect();
		}

		// ������ ����� �� �������
		String response = IdTime1->IOHandler->ReadLn();
		IdTime1->Disconnect();

		RichEdit1->Text = response;

		// ������ ����� ������� � �������� ����/�����
		TDateTime serverTime = ParseNistTimeResponse(response);

		// ����������� � ���������� ���� � �����
		LabeledEdit2->Text = serverTime.FormatString("yyyy-mm-dd");
		LabeledEdit3->Text = serverTime.FormatString("hh:nn:ss");

		Screen->Cursor = crDefault;
	}
	catch (Exception &e)
	{
		Screen->Cursor = crDefault;
		ShowMessage("������ ��� ��������� �������: " + e.Message +
				   "\n\n���������� ������ ������, ��������:\n- time.windows.com\n- pool.ntp.org\n- time.google.com");
	}
}

TDateTime TForm1::ParseNistTimeResponse(const String &response)
{
    // ������ ������ NIST: JJJJJ YY-MM-DD HH:MM:SS TT L H msADV UTC(NIST) *
    // ��������: 60798 25-05-03 21:39:18 50 0 0 539.0 UTC(NIST) *

    try {
        // ������� � ��� ��� �������
        // ShowMessage("������� ����� �� �������: " + response);

        // ��������� ������ �� ����� �� �������
        int spacePos1 = response.Pos(" ");
        if (spacePos1 <= 0) throw Exception("������������ ������ ������");

		int spacePos2 = response.Pos(" ", spacePos1 + 1);
        if (spacePos2 <= 0) throw Exception("������������ ������ ������");

        int spacePos3 = response.Pos(" ", spacePos2 + 1);
        if (spacePos3 <= 0) throw Exception("������������ ������ ������");

        // ��������� ���� � �����
        String dateStr = response.SubString(spacePos1 + 1, spacePos2 - spacePos1 - 1); // YY-MM-DD
        String timeStr = response.SubString(spacePos2 + 1, spacePos3 - spacePos2 - 1); // HH:MM:SS

        // �������� ���������� ����
        int firstDash = dateStr.Pos("-");
        int secondDash = dateStr.Pos("-", firstDash + 1);

        if (firstDash <= 0 || secondDash <= 0)
            throw Exception("������������ ������ ����");

        int yy = StrToIntDef(dateStr.SubString(1, firstDash - 1), 0);
        int mm = StrToIntDef(dateStr.SubString(firstDash + 1, secondDash - firstDash - 1), 0);
        int dd = StrToIntDef(dateStr.SubString(secondDash + 1, dateStr.Length() - secondDash), 0);

        // ����������� 2-�������� ��� � 4-��������
        int fullYear = (yy < 70) ? 2000 + yy : 1900 + yy;

        // �������� ���������� �������
        int firstColon = timeStr.Pos(":");
        int secondColon = timeStr.Pos(":", firstColon + 1);

        if (firstColon <= 0 || secondColon <= 0)
            throw Exception("������������ ������ �������");

        int hh = StrToIntDef(timeStr.SubString(1, firstColon - 1), 0);
        int mn = StrToIntDef(timeStr.SubString(firstColon + 1, secondColon - firstColon - 1), 0);
        int ss = StrToIntDef(timeStr.SubString(secondColon + 1, timeStr.Length() - secondColon), 0);

        // ������� TDateTime ������
        TDateTime result = EncodeDate(fullYear, mm, dd) + EncodeTime(hh, mn, ss, 0);

        return result;
    }
    catch (Exception &e)
    {
        throw Exception("������ ��� ������� ������ �� �������: " + e.Message + "\n�����: " + response);
    }
}

void __fastcall TForm1::Button2Click(TObject *Sender)
{
	try
	{
		// ���������, ��� ���� �� ������
		if (LabeledEdit2->Text.IsEmpty() || LabeledEdit3->Text.IsEmpty())
		{
			ShowMessage("������� �������� ����� � �������!");
            return;
        }

        // ������ ���� � ����� � TDateTime ������
        TDateTime dateTime;
        try
        {
            String dateTimeStr = LabeledEdit2->Text + " " + LabeledEdit3->Text;
            dateTime = StrToDateTime(dateTimeStr);
        }
        catch (...)
        {
            ShowMessage("�������� ������ ���� ��� �������!");
            return;
        }

        // ������������� ��������� �����
        SetSystemTime(dateTime);

        ShowMessage("����� ������� ����������������!");
    }
    catch (Exception &e)
    {
        ShowMessage("������ ��� ������������� �������: " + e.Message);
    }
}

void __fastcall TForm1::Timer1Timer(TObject *Sender)
{
    // ���������� ������� ���� �����
}

void TForm1::SetSystemTime(TDateTime DateTime)
{
    // ����������� TDateTime � ��������� SYSTEMTIME
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

    // ��� ��������� ���������� ������� ����� ����� ��������������
    if (!SetLocalTime(&st))
    {
        int error = GetLastError();
        throw Exception("�� ������� ���������� ��������� �����. ��� ������: " + IntToStr(error) +
                       "\n��������, ����� ����� ��������������.");
    }
}
