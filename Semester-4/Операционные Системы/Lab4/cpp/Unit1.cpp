//---------------------------------------------------------------------------

#include <windows.h>
#include <System.SysUtils.hpp>
#include <vcl.h>
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
    RichEdit1->Clear();

    // Установка форматирования для заголовков
    TFontStyles boldStyle;
    boldStyle << fsBold;

    // Информация о БИОС и процессоре
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("БИОС");
    RichEdit1->SelAttributes->Style = TFontStyles();
    RichEdit1->Lines->Add("Процессор");
    RichEdit1->Lines->Add("модель: S8 версия 31.12.99");
    RichEdit1->Lines->Add("дата выпуска: 2023");
    RichEdit1->Lines->Add("");

    // Информация о памяти
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("Память");
    RichEdit1->SelAttributes->Style = TFontStyles();

    MEMORYSTATUSEX memStatus;
    memStatus.dwLength = sizeof(memStatus);
    ::GlobalMemoryStatusEx(&memStatus);

    String memInfo = "ОЗУ: всего " + String((int)(memStatus.ullTotalPhys / (1024*1024))) +
        " МБ (" + String((int64_t)memStatus.ullTotalPhys) + " байт), свободно " +
        String((int)(memStatus.ullAvailPhys / (1024*1024))) + " МБ (" +
        String((int64_t)memStatus.ullAvailPhys) + " байт), занято " +
        String(memStatus.dwMemoryLoad) + "%";
    RichEdit1->Lines->Add(memInfo);

    // Дополнительная информация о виртуальной памяти
    String virtMemInfo = "Виртуальная память: всего " +
        String((int)(memStatus.ullTotalVirtual / (1024*1024))) + " МБ, свободно " +
        String((int)(memStatus.ullAvailVirtual / (1024*1024))) + " МБ";
    RichEdit1->Lines->Add(virtMemInfo);
    RichEdit1->Lines->Add("");

    // Имя компьютера
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("Имя компьютера");
    RichEdit1->SelAttributes->Style = TFontStyles();

    TCHAR computerName[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD size = MAX_COMPUTERNAME_LENGTH + 1;
    ::GetComputerNameW(computerName, &size);
    RichEdit1->Lines->Add(String(computerName));
    RichEdit1->Lines->Add("");

    // Имя пользователя
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("Имя пользователя");
    RichEdit1->SelAttributes->Style = TFontStyles();

    TCHAR userName[256];
    DWORD userSize = 256;
    ::GetUserNameW(userName, &userSize);
    RichEdit1->Lines->Add(String(userName));
    RichEdit1->Lines->Add("");

    // Информация о системе
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("Информация о системе");
    RichEdit1->SelAttributes->Style = TFontStyles();

    OSVERSIONINFOEX osInfo;
    ZeroMemory(&osInfo, sizeof(OSVERSIONINFOEX));
    osInfo.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);

    #pragma warning(disable: 4996) // Для обхода предупреждения о устаревшей функции
    GetVersionEx((OSVERSIONINFO*)&osInfo);

    RichEdit1->Lines->Add("Версия Windows: " + String(osInfo.dwMajorVersion) + "." +
        String(osInfo.dwMinorVersion) + " (Build " + String(osInfo.dwBuildNumber) + ")");

    // Определение количества процессоров
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    RichEdit1->Lines->Add("Количество процессоров: " + String(sysInfo.dwNumberOfProcessors));
    RichEdit1->Lines->Add("");

    // Информация о дисках
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("Жесткий диск");
    RichEdit1->SelAttributes->Style = TFontStyles();

    String drive = ExtractFileDrive(Application->ExeName) + "\\";
    ULARGE_INTEGER freeBytes, totalBytes;
    ::GetDiskFreeSpaceExW(drive.c_str(), &freeBytes, &totalBytes, NULL);

    ULARGE_INTEGER usedBytes;
    usedBytes.QuadPart = totalBytes.QuadPart - freeBytes.QuadPart;

    RichEdit1->Lines->Add("Диск " + drive);
    RichEdit1->Lines->Add("Объем диска: " + String((int)(totalBytes.QuadPart / (1024*1024*1024))) + " ГБ");
    RichEdit1->Lines->Add("Свободно: " + String((int)(freeBytes.QuadPart / (1024*1024*1024))) + " ГБ");
    RichEdit1->Lines->Add("Занято: " + String((int)(usedBytes.QuadPart / (1024*1024*1024))) + " ГБ");
    RichEdit1->Lines->Add("Процент использования: " +
        String((int)(100.0 * usedBytes.QuadPart / totalBytes.QuadPart)) + "%");

    // Перебор всех дисков в системе
    RichEdit1->Lines->Add("");
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("Все доступные диски:");
    RichEdit1->SelAttributes->Style = TFontStyles();

    DWORD drives = GetLogicalDrives();
    for (int i = 0; i < 26; i++) {
        if ((drives & (1 << i)) != 0) {
            String driveLetter = String((char)('A' + i)) + ":\\";
            UINT driveType = GetDriveType(driveLetter.c_str());
            String driveTypeStr;

            switch (driveType) {
                case DRIVE_FIXED: driveTypeStr = "Локальный диск"; break;
                case DRIVE_REMOVABLE: driveTypeStr = "Съемный диск"; break;
                case DRIVE_REMOTE: driveTypeStr = "Сетевой диск"; break;
                case DRIVE_CDROM: driveTypeStr = "CD/DVD"; break;
                default: driveTypeStr = "Другой тип"; break;
            }

            RichEdit1->Lines->Add(driveLetter + " - " + driveTypeStr);
        }
    }

    // Информация о времени работы системы
    RichEdit1->Lines->Add("");
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("Время работы системы:");
    RichEdit1->SelAttributes->Style = TFontStyles();

    DWORD tickCount = GetTickCount();
    int days = tickCount / (1000 * 60 * 60 * 24);
    int hours = (tickCount % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60);
    int minutes = (tickCount % (1000 * 60 * 60)) / (1000 * 60);

    RichEdit1->Lines->Add("Компьютер работает: " + String(days) + " дн. " +
        String(hours) + " ч. " + String(minutes) + " мин.");
}
