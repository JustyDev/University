import win32api
import win32con
import win32security

def get_logged_users():
    users = []
    try:
        hToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32con.TOKEN_QUERY)
        user_sid, _ = win32security.GetTokenInformation(hToken, win32security.TokenUser)
        user_name, domain, _ = win32security.LookupAccountSid(None, user_sid)
        users.append(f"{domain}\\{user_name}")
        win32api.CloseHandle(hToken)
    except win32api.error:
        pass
    return users

if __name__ == "__main__":
    users = get_logged_users()
    for user in users:
        print(f"Пользователь: {user}")
