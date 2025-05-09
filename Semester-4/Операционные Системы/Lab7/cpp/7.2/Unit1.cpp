//---------------------------------------------------------------------------

#include <vcl.h>
#include <windows.h>
#include <processenv.h>
#include <lmcons.h>
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
void __fastcall TForm1::Button1Click(TObject *Sender)
{
    wchar_t platform[128];
    wchar_t processor[128];
    wchar_t systemDir[MAX_PATH];
    wchar_t userName[UNLEN + 1];
    wchar_t computerName[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD size;

    GetEnvironmentVariableW(L"PROCESSOR_ARCHITECTURE", platform, 128);

	GetEnvironmentVariableW(L"PROCESSOR_IDENTIFIER", processor, 128);

    GetSystemDirectoryW(systemDir, MAX_PATH);

	size = UNLEN + 1;
    GetUserNameW(userName, &size);

    size = MAX_COMPUTERNAME_LENGTH + 1;
    GetComputerNameW(computerName, &size);

    Memo1->Lines->Clear();
    Memo1->Lines->Add(L"Платформа ОС: " + String(platform));
    Memo1->Lines->Add(L"Описание процессора: " + String(processor));
    Memo1->Lines->Add(L"Системный каталог: " + String(systemDir));
    Memo1->Lines->Add(L"Имя пользователя: " + String(userName));
    Memo1->Lines->Add(L"Имя компьютера: " + String(computerName));
}
//---------------------------------------------------------------------------
