#include <Windows.h>
#include <iostream>

int main(int argc, char* argv[]) {
    HWND hwnd = FindWindowW(NULL, L"GitHub Desktop");
    if (!hwnd) {
        std::cout << "Error find window\n";
        return 1;
    }

    std::cout << "HWND=" << std::hex << hwnd << "\n";

    // Получаем ID процесса
    DWORD id;
    GetWindowThreadProcessId(hwnd, &id);

    // Получаем хэндл процесса
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, id);
    if (!hProcess) {
        std::cout << "Error get handle process\n";
        return 1;
    }

    std::cout << "hProcess=" << std::hex << hProcess << "\n";

    // Получаем информацию о времени работы процесса
    FILETIME ft[4];
    if (!GetProcessTimes(hProcess, &ft[0], &ft[1], &ft[2], &ft[3])) {
        std::cout << "Error getting process times\n";
        CloseHandle(hProcess);
        return 1;
    }

    SYSTEMTIME tm[4];
    FileTimeToLocalFileTime(&(ft[0]), &(ft[0]));
    for (int i = 0; i < 4; i++) {
        FileTimeToSystemTime(&(ft[i]), &(tm[i]));
    }

    // Выводим время создания процесса
    printf("Created at %02d:%02d:%02d\n", tm[0].wHour, tm[0].wMinute, tm[0].wSecond);

    // Выводим время процессора (ядро и пользователь)
    printf("Kernel time %02d:%02d:%02d:%02d\n", tm[2].wHour, tm[2].wMinute, tm[2].wSecond, tm[2].wMilliseconds);
    printf("User time %02d:%02d:%02d:%02d\n", tm[3].wHour, tm[3].wMinute, tm[3].wSecond, tm[3].wMilliseconds);

    TerminateProcess(hProcess, NO_ERROR);
    CloseHandle(hProcess);

    return 0;
}
