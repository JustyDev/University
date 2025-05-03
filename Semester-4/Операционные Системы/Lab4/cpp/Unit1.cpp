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

    // ��������� �������������� ��� ����������
    TFontStyles boldStyle;
    boldStyle << fsBold;

    // ���������� � ���� � ����������
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("����");
    RichEdit1->SelAttributes->Style = TFontStyles();
    RichEdit1->Lines->Add("���������");
    RichEdit1->Lines->Add("������: S8 ������ 31.12.99");
    RichEdit1->Lines->Add("���� �������: 2023");
    RichEdit1->Lines->Add("");

    // ���������� � ������
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("������");
    RichEdit1->SelAttributes->Style = TFontStyles();

    MEMORYSTATUSEX memStatus;
    memStatus.dwLength = sizeof(memStatus);
    ::GlobalMemoryStatusEx(&memStatus);

    String memInfo = "���: ����� " + String((int)(memStatus.ullTotalPhys / (1024*1024))) +
        " �� (" + String((int64_t)memStatus.ullTotalPhys) + " ����), �������� " +
        String((int)(memStatus.ullAvailPhys / (1024*1024))) + " �� (" +
        String((int64_t)memStatus.ullAvailPhys) + " ����), ������ " +
        String(memStatus.dwMemoryLoad) + "%";
    RichEdit1->Lines->Add(memInfo);

    // �������������� ���������� � ����������� ������
    String virtMemInfo = "����������� ������: ����� " +
        String((int)(memStatus.ullTotalVirtual / (1024*1024))) + " ��, �������� " +
        String((int)(memStatus.ullAvailVirtual / (1024*1024))) + " ��";
    RichEdit1->Lines->Add(virtMemInfo);
    RichEdit1->Lines->Add("");

    // ��� ����������
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("��� ����������");
    RichEdit1->SelAttributes->Style = TFontStyles();

    TCHAR computerName[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD size = MAX_COMPUTERNAME_LENGTH + 1;
    ::GetComputerNameW(computerName, &size);
    RichEdit1->Lines->Add(String(computerName));
    RichEdit1->Lines->Add("");

    // ��� ������������
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("��� ������������");
    RichEdit1->SelAttributes->Style = TFontStyles();

    TCHAR userName[256];
    DWORD userSize = 256;
    ::GetUserNameW(userName, &userSize);
    RichEdit1->Lines->Add(String(userName));
    RichEdit1->Lines->Add("");

    // ���������� � �������
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("���������� � �������");
    RichEdit1->SelAttributes->Style = TFontStyles();

    OSVERSIONINFOEX osInfo;
    ZeroMemory(&osInfo, sizeof(OSVERSIONINFOEX));
    osInfo.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);

    #pragma warning(disable: 4996) // ��� ������ �������������� � ���������� �������
    GetVersionEx((OSVERSIONINFO*)&osInfo);

    RichEdit1->Lines->Add("������ Windows: " + String(osInfo.dwMajorVersion) + "." +
        String(osInfo.dwMinorVersion) + " (Build " + String(osInfo.dwBuildNumber) + ")");

    // ����������� ���������� �����������
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    RichEdit1->Lines->Add("���������� �����������: " + String(sysInfo.dwNumberOfProcessors));
    RichEdit1->Lines->Add("");

    // ���������� � ������
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("������� ����");
    RichEdit1->SelAttributes->Style = TFontStyles();

    String drive = ExtractFileDrive(Application->ExeName) + "\\";
    ULARGE_INTEGER freeBytes, totalBytes;
    ::GetDiskFreeSpaceExW(drive.c_str(), &freeBytes, &totalBytes, NULL);

    ULARGE_INTEGER usedBytes;
    usedBytes.QuadPart = totalBytes.QuadPart - freeBytes.QuadPart;

    RichEdit1->Lines->Add("���� " + drive);
    RichEdit1->Lines->Add("����� �����: " + String((int)(totalBytes.QuadPart / (1024*1024*1024))) + " ��");
    RichEdit1->Lines->Add("��������: " + String((int)(freeBytes.QuadPart / (1024*1024*1024))) + " ��");
    RichEdit1->Lines->Add("������: " + String((int)(usedBytes.QuadPart / (1024*1024*1024))) + " ��");
    RichEdit1->Lines->Add("������� �������������: " +
        String((int)(100.0 * usedBytes.QuadPart / totalBytes.QuadPart)) + "%");

    // ������� ���� ������ � �������
    RichEdit1->Lines->Add("");
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("��� ��������� �����:");
    RichEdit1->SelAttributes->Style = TFontStyles();

    DWORD drives = GetLogicalDrives();
    for (int i = 0; i < 26; i++) {
        if ((drives & (1 << i)) != 0) {
            String driveLetter = String((char)('A' + i)) + ":\\";
            UINT driveType = GetDriveType(driveLetter.c_str());
            String driveTypeStr;

            switch (driveType) {
                case DRIVE_FIXED: driveTypeStr = "��������� ����"; break;
                case DRIVE_REMOVABLE: driveTypeStr = "������� ����"; break;
                case DRIVE_REMOTE: driveTypeStr = "������� ����"; break;
                case DRIVE_CDROM: driveTypeStr = "CD/DVD"; break;
                default: driveTypeStr = "������ ���"; break;
            }

            RichEdit1->Lines->Add(driveLetter + " - " + driveTypeStr);
        }
    }

    // ���������� � ������� ������ �������
    RichEdit1->Lines->Add("");
    RichEdit1->SelAttributes->Style = boldStyle;
    RichEdit1->Lines->Add("����� ������ �������:");
    RichEdit1->SelAttributes->Style = TFontStyles();

    DWORD tickCount = GetTickCount();
    int days = tickCount / (1000 * 60 * 60 * 24);
    int hours = (tickCount % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60);
    int minutes = (tickCount % (1000 * 60 * 60)) / (1000 * 60);

    RichEdit1->Lines->Add("��������� ��������: " + String(days) + " ��. " +
        String(hours) + " �. " + String(minutes) + " ���.");
}
