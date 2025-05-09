import win32file
import win32net

def get_network_connections():
    connections = []
    resume_handle = 0
    level = 1
    try:
        while True:
            network_connections, total_resume, resume_handle = win32net.NetUseEnum(None, level, resume_handle)
            print(network_connections, total_resume, resume_handle)
            for connection in network_connections:
                local_name = connection.get('local', '')
                remote_name = connection.get('remote', '')
                status = get_connection_status(remote_name)
                connections.append((local_name, remote_name, status))
            if not resume_handle:
                break
    except Exception as e:
        print(f"Ошибка при получении сетевых подключений: {e}")
    return connections

def get_connection_status(remote_name):
    try:
        win32file.GetFileAttributes(remote_name)
        return "Подключено"
    except Exception:
        return "Отключено"

connections = get_network_connections()
for local_name, remote_name, status in connections:
    print(f"Локальное имя: {local_name}, Удаленное имя: {remote_name}, Статус: {status}")
