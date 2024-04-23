import time
from random import random
from math import sqrt

# измерение времени работы
start_time = time.time()
m = 0  # успешные результаты

N = 10_000_000
l = 1  # длина катетов AB и AC, условие

for _ in range(N):
    # случайная генерация положения M
    M = random()
    # если сумма длин сторон меньше 3-х
    if (M + l + sqrt(M ** 2 + l ** 2)) < 3:
        m += 1

# расчёт времени выполнения
execution_time = time.time() - start_time  # вычисляем время выполнения

print("Имитация:", m / N)
print("Ручной расчёт:", 3/4)
print(f"Время выполнения: {execution_time} секунд")
