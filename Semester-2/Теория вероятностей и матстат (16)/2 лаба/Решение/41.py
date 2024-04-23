import time

# измерение времени работы
start_time = time.time()

x, y = 0, 0  # моменты поступления первого и второго сигналов
T = 200  # длительность работы
t = 30  # какая-то переменная
arr = []  # массив успешных координат


# имеется ли нужная координата в массиве координат
def isExist(sx, sy, s_arr):
    for xy in s_arr:
        if sx == xy[0] and sy == xy[1]:
            return True
    return False


for x in range(0, T):
    for y in range(0, T):
        if (y < x + t and y > x) or (y > x - t and y < x):
            arr.append([x, y])

lines = []

for x in range(0, T):
    line = [int(isExist(x, y, arr)) for y in range(0, T)]
    lines.insert(0, line)

print("Схема:")
[print(l) for l in lines]

execution_time = time.time() - start_time  # вычисляем время выполнения

print("Площадь g:", t * (2 * T - t))
print("Площадь G:", T ** 2)
print("Вероятность (g/G):", t * (2 * T - t) / T ** 2)
print("Вероятность по точкам:", len(arr) / T ** 2)
print(f"Время выполнения: {execution_time} секунд")
