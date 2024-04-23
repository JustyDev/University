import time
from random import uniform

# измерение времени работы
start_time = time.time()
m = 0  # успешные результаты

N = 10_000_000
T = 100
t = 30

for _ in range(N):
    # случайная генерация x и y
    x, y = uniform(1, T), uniform(1, T)

    # входят ли x и y в область шестиугольника
    if (x + t > y > x) or (x - t < y < x):
        m += 1

# расчёт времени выполнения
execution_time = time.time() - start_time

print("Имитация:", m / N)
print("Ручной расчёт:", t * (2 * T - t) / T ** 2)
print(f"Время выполнения: {execution_time} секунд")
