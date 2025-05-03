import platform
import os
import psutil
import socket
import getpass
import datetime


def print_header(text):
    """Функция для печати заголовка с выделением (жирный шрифт в консоли)"""
    # ANSI-код для жирного текста: \033[1m
    # ANSI-код для сброса форматирования: \033[0m
    if os.name == 'nt':  # Windows может не поддерживать ANSI в некоторых консолях
        print(text)
    else:
        print(f"\033[1m{text}\033[0m")


def show_system_info():
    """Выводит информацию о системе в консоль"""

    # Информация о БИОС и процессоре
    print_header("БИОС")
    print("Процессор")
    print(f"модель: {platform.processor()}")
    print(f"дата выпуска: {datetime.datetime.now().year}")
    print()

    # Информация о памяти
    print_header("Память")
    mem = psutil.virtual_memory()
    total_mb = mem.total // (1024 * 1024)
    available_mb = mem.available // (1024 * 1024)
    print(
        f"ОЗУ: всего {total_mb} МБ ({mem.total} байт), свободно {available_mb} МБ ({mem.available} байт), занято {mem.percent}%")

    # Дополнительная информация о виртуальной памяти
    swap = psutil.swap_memory()
    swap_total_mb = swap.total // (1024 * 1024)
    swap_free_mb = swap.free // (1024 * 1024)
    print(f"Виртуальная память: всего {swap_total_mb} МБ, свободно {swap_free_mb} МБ")
    print()

    # Имя компьютера
    print_header("Имя компьютера")
    print(f"{socket.gethostname()}")
    print()

    # Имя пользователя
    print_header("Имя пользователя")
    print(f"{getpass.getuser()}")
    print()

    # Информация о системе
    print_header("Информация о системе")
    print(f"Операционная система: {platform.system()} {platform.release()} (Версия {platform.version()})")
    print(f"Архитектура: {platform.architecture()[0]}")
    print(f"Количество процессоров: {os.cpu_count()}")
    print()

    # Информация о дисках
    print_header("Жесткий диск")

    # Основной диск (где запущена программа)
    root_path = os.path.abspath(os.sep)
    disk_usage = psutil.disk_usage(root_path)
    total_gb = disk_usage.total // (1024 ** 3)
    free_gb = disk_usage.free // (1024 ** 3)
    used_gb = disk_usage.used // (1024 ** 3)

    print(f"Диск {root_path}")
    print(f"Объем диска: {total_gb} ГБ")
    print(f"Свободно: {free_gb} ГБ")
    print(f"Занято: {used_gb} ГБ")
    print(f"Процент использования: {disk_usage.percent}%")
    print()

    # Все доступные диски
    print_header("Все доступные диски:")

    for partition in psutil.disk_partitions():
        if os.name == 'nt':
            # Windows
            drive_type = "Неизвестно"
            try:
                if "fixed" in partition.opts:
                    drive_type = "Локальный диск"
                elif "cdrom" in partition.opts:
                    drive_type = "CD/DVD"
                elif "removable" in partition.opts:
                    drive_type = "Съемный диск"
                print(f"{partition.device} - {drive_type}")
            except:
                pass
        else:
            # Unix/Linux/Mac
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"{partition.mountpoint} - {partition.fstype} - {usage.percent}% использовано")
            except:
                print(f"{partition.mountpoint} - {partition.fstype}")
    print()

    # Информация о времени работы системы
    print_header("Время работы системы:")

    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = now - boot_time
    days, remainder = divmod(uptime.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds = int(remainder)

    print(f"Компьютер работает: {int(days)} дн. {int(hours)} ч. {int(minutes)} мин. {seconds} сек.")
    print(f"Время запуска: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Информация о сети
    print()
    print_header("Информация о сети:")

    # Получение IP-адресов
    hostname = socket.gethostname()
    print(f"Имя хоста: {hostname}")
    try:
        print(f"IPv4-адрес: {socket.gethostbyname(hostname)}")
    except:
        print("IPv4-адрес: не доступен")

    # Сетевые интерфейсы
    print("Сетевые интерфейсы:")
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  {interface_name}: {address.address}")

print("=== Информация о системе ===\n")
try:
    show_system_info()
except Exception as e:
    print(f"Произошла ошибка при получении информации о системе: {e}")

# Ждем ввода пользователя перед закрытием программы
if os.name == 'nt':  # Windows
    input("\nНажмите Enter для выхода...")