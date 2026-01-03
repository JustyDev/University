import random
# --------------------------- ФУНКЦИЯ МЁБИУСА ---------------------------

def mobius(n):
    i = 2
    cnt = 0
    x = n
    while i * i <= x:
        if x % i == 0:
            cnt += 1
            x //= i
            if x % i == 0:
                return 0
        else:
            i += 1
    if x > 1:
        cnt += 1
    return -1 if cnt % 2 else 1


def mobius_table(n):
    print("\nТАБЛИЦА µ(k):")
    print("k | µ(k)\n----------")
    for k in range(1, n + 1):
        print(k, "|", mobius(k))


# --------------------------- ПРОВЕРКА НА ПРОСТОТУ ---------------------------

def is_probable_prime(n, k=5):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# --------------------------- ГЕНЕРАЦИЯ ПРОСТЫХ ---------------------------

def generate_prime(bits=16):
    while True:
        p = random.getrandbits(bits)
        if is_probable_prime(p):
            return p


# --------------------------- ОБРАТНОЕ ЧИСЛО ---------------------------

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def mod_inverse(e, phi):
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception("Обратного числа не существует")
    return x % phi


# --------------------------- RSA ---------------------------

def generate_rsa_keys(bits=16):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while egcd(e, phi)[0] != 1:
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)
    return (e, n), (d, n), (p, q, phi)


def encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)


def decrypt(cipher, private_key):
    d, n = private_key
    return pow(cipher, d, n)


# --------------------------- MAIN ---------------------------

if __name__ == "__main__":
    print("\n=== ФУНКЦИЯ МЁБИУСА ===")
    mobius_table(30)

    print("\n=== СОЗДАНИЕ RSA-КЛЮЧЕЙ ===")
    public, private, info = generate_rsa_keys(bits=16)

    p, q, phi = info

    print(f"\nПростые p = {p}, q = {q}")
    print(f"n = p*q = {p * q}")
    print(f"φ(n) = {phi}")
    print("Открытый ключ:", public)
    print("Закрытый ключ:", private)

    print("\n=== ШИФРОВАНИЕ И ДЕШИФРОВАНИЕ ЧИСЛА ===")
    message = 42
    cipher = encrypt(message, public)
    original = decrypt(cipher, private)

    print("Сообщение:", message)
    print("Зашифрованное:", cipher)
    print("Расшифрованное:", original)

    print("\n=== ШИФРОВАНИЕ СТРОКИ ===")
    text = "HELLO"

    encoded = [encrypt(ord(ch), public) for ch in text]
    decoded = "".join(chr(decrypt(x, private)) for x in encoded)

    print("Исходный текст:", text)
    print("В шифре:", encoded)
    print("После расшифровки:", decoded)