from numpy import random
import time

# измерение времени работы
start_time = time.time()

N = 10_000_000
m1, m2 = 0, 0

for X in random.binomial(n=7, p=.2, size=N):
    if 1 < X < 4:
        m1 += 1

for X in random.binomial(n=7, p=.2, size=N):
    if 0 < X < 8:
        m2 += 1

# расчёт времени выполнения
execution_time = time.time() - start_time

print("Вероятность (1 < X < 4):", m1 / N)
print("Вероятность (0 < X < 8):", m2 / N)
print("Вероятность:", m2 / N * m1 / N)
print(f"Время выполнения: {execution_time} секунд")
