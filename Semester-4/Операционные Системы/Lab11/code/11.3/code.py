import win32gui
import win32process
import win32api
import psutil
import time

def get_process_info_and_terminate(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print("Error find window")
        return
    print(f"HWND = {hwnd}")
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    print(f"PID = {pid}")
    try:
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print("Error get handle process!")
        return
    print(f"Created at: {time.ctime(process.create_time())}")
    print(f"User time: {process.cpu_times().user:.2f} сек")
    print(f"Kernel time: {process.cpu_times().system:.2f} сек")
    try:
        process.terminate()
    except Exception as e:
        print(f"Error")
        
if __name__ == "__main__":
    target_window = "GitHub Desktop"
    get_process_info_and_terminate(target_window)
