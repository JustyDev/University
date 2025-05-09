import socket
import struct
import time
import sys
import ctypes
import datetime
import win32api


def get_ntp_time(server="pool.ntp.org", port=123):
    """
    Получение точного времени с NTP сервера
    """
    # NTP запрос происходит в виде 48-байтного пакета
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5.0)

    # Формируем NTP пакет
    # Первый байт включает в себя версию и режим
    # Версия 3, режим клиента = 3
    packet = b'\x1b' + 47 * b'\0'

    try:
        # Отправляем запрос
        client.sendto(packet, (server, port))
        # Получаем ответ
        packet, _ = client.recvfrom(1024)
    except socket.timeout:
        print(f"Ошибка: Время ожидания ответа от {server} истекло.")
        return None
    except socket.gaierror:
        print(f"Ошибка: Не удалось разрешить имя сервера {server}.")
        return None
    except Exception as e:
        print(f"Ошибка при получении времени: {e}")
        return None
    finally:
        client.close()

    if not packet:
        return None

    # Распаковываем ответ: нас интересуют байты с 40-го по 43-й,
    # которые представляют собой timestamp передачи пакета сервером
    seconds = struct.unpack('!12I', packet)[10]
    # NTP использует эпоху, которая начинается с 1900-01-01
    # Unix время начинается с 1970-01-01, поэтому мы вычитаем разницу
    seconds -= 2208988800

    return seconds


def set_system_time(seconds):
    """
    Установка системного времени с помощью pywin32
    """
    try:
        # Конвертация Unix timestamp в локальное время
        local_time = time.localtime(seconds)

        # Создаем структуру SYSTEMTIME для win32api
        system_time = win32api.GetSystemTime()

        # Обновляем время
        new_time = (
            local_time.tm_year,
            local_time.tm_mon,
            0,  # Не используется в SYSTEMTIME
            local_time.tm_mday,
            local_time.tm_hour,
            local_time.tm_min,
            local_time.tm_sec,
            0  # Миллисекунды
        )

        # Устанавливаем системное время
        win32api.SetSystemTime(*new_time)

        return True
    except Exception as e:
        print(f"Ошибка при установке системного времени: {e}")
        return False


def check_admin_privileges():
    """
    Проверка прав администратора
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def main():
    """
    Основная функция программы
    """
    print("Программа синхронизации времени с NTP сервером")
    print("----------------------------------------------")

    # Проверка прав администратора
    if not check_admin_privileges():
        print("Ошибка: Для синхронизации времени требуются права администратора.")
        print("Пожалуйста, запустите программу от имени администратора.")
        return

    # Получение текущего времени компьютера
    current_time = time.time()
    local_time = time.localtime(current_time)
    print(f"Текущее время компьютера: {time.strftime('%Y-%m-%d %H:%M:%S', local_time)}")

    # Выбор сервера NTP
    server = input("Введите адрес NTP сервера (или нажмите Enter для использования pool.ntp.org): ")
    if not server:
        server = "pool.ntp.org"

    print(f"Подключение к серверу {server}...")

    # Получение времени с NTP сервера
    ntp_seconds = get_ntp_time(server)

    if ntp_seconds is None:
        print("Не удалось получить время с NTP сервера.")
        return

    ntp_time = time.localtime(ntp_seconds)
    print(f"Время с NTP сервера: {time.strftime('%Y-%m-%d %H:%M:%S', ntp_time)}")

    # Вычисление разницы во времени
    time_diff = abs(current_time - ntp_seconds)
    print(f"Разница во времени: {time_diff:.3f} секунд")

    # Синхронизация времени
    prompt = input("Синхронизировать время компьютера с сервером? (y/n): ")
    if prompt.lower() == 'y':
        print("Синхронизация времени...")
        if set_system_time(ntp_seconds):
            print("Время успешно синхронизировано!")

            # Показываем обновленное время
            updated_time = time.localtime(time.time())
            print(f"Новое время компьютера: {time.strftime('%Y-%m-%d %H:%M:%S', updated_time)}")
        else:
            print("Не удалось синхронизировать время.")
    else:
        print("Синхронизация отменена.")


main()