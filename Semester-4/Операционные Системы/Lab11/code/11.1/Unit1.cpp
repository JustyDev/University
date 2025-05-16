#include <vcl.h>
#include <tlhelp32.h>
#include <Psapi.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;

TNotifyIconData NID;
PInf *Inf;

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
 : TForm(Owner)
{
}

void __fastcall TForm1::MTIcon(TMessage &a)
{
    switch (a.LParam)
    {
        case WM_LBUTTONDBLCLK:
        case WM_RBUTTONDOWN:
            Form1->Show();
            SetForegroundWindow(Handle);
            break;
    }
}

void __fastcall TForm1::spisokprocessov()
{
    for (int i = 0; i < ListBox1->Count; i++) {
        PInf* item = (PInf*)(ListBox1->Items->Objects[i]);
        if (item && item->H) CloseHandle(item->H);
        delete item;
    }

    ListBox1->Clear();

    HANDLE HS = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (HS == INVALID_HANDLE_VALUE) return;

    PROCESSENTRY32 P;
    P.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(HS, &P)) {
        do {
            HANDLE hProcess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, P.th32ProcessID);
            if (hProcess) {
                PInf *inf = new PInf;
                inf->Usage = P.cntUsage;
                inf->Threads = P.cntThreads;
                inf->PriClassBase = P.pcPriClassBase;
                inf->ID = P.th32ProcessID;
                inf->Suspended = false;
                inf->H = hProcess;

                FILETIME ftCreate, ftExit, ftKernel, ftUser;
                if (GetProcessTimes(hProcess, &ftCreate, &ftExit, &ftKernel, &ftUser)) {
                    inf->StartTime = ftCreate;
                } else {
                    ZeroMemory(&inf->StartTime, sizeof(FILETIME));
                }

				ListBox1->AddItem(P.szExeFile, (TObject*)inf);
            }
        } while (Process32Next(HS, &P));
    }

    CloseHandle(HS);
}

__int64 FileTimeToInt64(FILETIME ft)
{
    ULARGE_INTEGER uli;
    uli.LowPart = ft.dwLowDateTime;
    uli.HighPart = ft.dwHighDateTime;
    return uli.QuadPart;
}

void __fastcall TForm1::FormCreate(TObject *Sender)
{
    Application->ShowMainForm = true;
    NID.cbSize = sizeof(TNotifyIconData);
    NID.hWnd = Handle;
    NID.uID = 1;
    NID.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;
    NID.uCallbackMessage = WM_USER + 1;
    NID.hIcon = Application->Icon->Handle;
    wcscpy(NID.szTip, L"Terminate Process");
    Shell_NotifyIcon(NIM_ADD, &NID);

    spisokprocessov();
}

void __fastcall TForm1::Timer1Timer(TObject *Sender)
{
    spisokprocessov();

    FILETIME ftNow;
    GetSystemTimeAsFileTime(&ftNow);

    for (int i = 0; i < ListBox1->Count; i++) {
        AnsiString procName = ListBox1->Items->Strings[i];
        if (procName == "notepad.exe") {
            PInf* inf = (PInf*)ListBox1->Items->Objects[i];

            if (inf && inf->H) {
                __int64 now = FileTimeToInt64(ftNow);
                __int64 start = FileTimeToInt64(inf->StartTime);

                if (now - start > 1200000000) {
                    TerminateProcess(inf->H, 1);
                    WaitForSingleObject(inf->H, 3000);
                }
            }
        }
    }

    spisokprocessov();
}

void __fastcall TForm1::Button1Click(TObject *Sender)
{
    Form1->Visible = false;
}

void __fastcall TForm1::Button2Click(TObject *Sender)
{
    Form1->Close();
}

void __fastcall TForm1::FormDestroy(TObject *Sender)
{
	Shell_NotifyIcon(NIM_DELETE, &NID);
}
//---------------------------------------------------------------------------

