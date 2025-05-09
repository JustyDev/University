//---------------------------------------------------------------------------

#include <vcl.h>
#include <SysUtils.hpp>
#include <VersionHelpers.h>
#include <windows.h>
#include <lmcons.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;
//---------------------------------------------------------------------------
typedef LONG(WINAPI *RtlGetVersionPtr)(PRTL_OSVERSIONINFOW);
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Button1Click(TObject *Sender)
{
	RTL_OSVERSIONINFOW osvi = { 0 };
    osvi.dwOSVersionInfoSize = sizeof(osvi);

    HMODULE hMod = GetModuleHandle(L"ntdll.dll");
    if (hMod) {
        RtlGetVersionPtr fPtr = (RtlGetVersionPtr)GetProcAddress(hMod, "RtlGetVersion");
        if (fPtr) {
            fPtr(&osvi);
        }
    }

    wchar_t systemDir[MAX_PATH];
    GetSystemDirectoryW(systemDir, MAX_PATH);

    DWORD size = MAX_COMPUTERNAME_LENGTH + 1;
    wchar_t computerName[MAX_COMPUTERNAME_LENGTH + 1];
    GetComputerNameW(computerName, &size);

    size = UNLEN + 1;
    wchar_t userName[UNLEN + 1];
    GetUserNameW(userName, &size);

    SYSTEM_INFO siSysInfo;
    GetNativeSystemInfo(&siSysInfo);

	__int64 totalDiskSpace = DiskSize(3);
	__int64 freeDiskSpace = DiskFree(3);

	String platform;
	switch (osvi.dwPlatformId) {
		case VER_PLATFORM_WIN32_NT: platform = "Windows NT-based (2000, XP, Vista, 7, 8, 10, 11)"; break;
		case VER_PLATFORM_WIN32_WINDOWS: platform = "Windows 95, 98, Me"; break;
		case VER_PLATFORM_WIN32s: platform = "Windiows 3.x"; break;
		default: platform = L"Неизвестная платформа"; break;
	}

	String cpuArch;
	switch (siSysInfo.wProcessorArchitecture) {
		case PROCESSOR_ARCHITECTURE_AMD64: cpuArch = "x64 (64-bit)"; break;
		case PROCESSOR_ARCHITECTURE_INTEL: cpuArch = "x86 (32-bit)"; break;
		case PROCESSOR_ARCHITECTURE_ARM: cpuArch = "ARM"; break;
		case PROCESSOR_ARCHITECTURE_ARM64: cpuArch = "ARM64"; break;
		default: cpuArch = L"Неизвестная архитектура"; break;
	}

    Memo1->Lines->Clear();
	Memo1->Lines->Add(L"Название и версия ОС: " + String(osvi.dwMajorVersion) + "." + String(osvi.dwMinorVersion) + " (Build " + String(osvi.dwBuildNumber) + ")");
	Memo1->Lines->Add(L"Платформа ОС: " + platform);
	Memo1->Lines->Add(L"Описание процессора: Архитектура " + cpuArch);
	Memo1->Lines->Add(L"Системный каталог: " + String(systemDir));
	Memo1->Lines->Add(L"Имя пользователя: " + String(userName));
	Memo1->Lines->Add(L"Имя компьютера: " + String(computerName));
	Memo1->Lines->Add(L"Размер текущего диска (байт): " + String(totalDiskSpace));
	Memo1->Lines->Add(L"Свободное место на текущем диске (байт): " + String(freeDiskSpace));
}
//---------------------------------------------------------------------------
