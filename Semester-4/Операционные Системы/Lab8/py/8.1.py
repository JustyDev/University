import win32api
import win32process
import win32con

def get_process_list():
    processes = []
    snapshot = win32process.EnumProcesses()
    for pid in snapshot:
        try:
            hProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
            modules = win32process.EnumProcessModules(hProcess)
            exe_name = win32process.GetModuleFileNameEx(hProcess, modules[0]) if modules else "Unknown"
            processes.append((pid, exe_name))
            win32api.CloseHandle(hProcess)
        except (win32api.error, IndexError):
            continue
    return processes

def get_process_details(pid):
    try:
        hProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
        modules = win32process.EnumProcessModules(hProcess)
        process_name = win32process.GetModuleFileNameEx(hProcess, modules[0]) if modules else "Unknown"
        win32api.CloseHandle(hProcess)
        return f"PID: {pid}, Имя процесса: {process_name}"
    except win32api.error:
        return f"PID: {pid}, Имя процесса: Недоступно"

if __name__ == "__main__":
    process_list = get_process_list()
    for pid, process_name in process_list:
        print(get_process_details(pid))
