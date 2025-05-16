import win32file

def get_disk_space(drive):
    free_bytes, total_bytes, _ = win32file.GetDiskFreeSpaceEx(drive)
    percent_free = (free_bytes / total_bytes) * 100
    free_bytes /= 1000**3
    total_bytes /= 1000**3
    return f"Диск: {drive}, Всего: {round(total_bytes, 2)} ГБ, Свободно: {round(free_bytes, 2)} ГБ, {percent_free:.1f}% свободно"

# Пример использования
print(get_disk_space("C:\\"))
