# P = t*(2*T - t) / T**2
# искомая вероятность в ручном расчёте

x, y = 0, 0  # моменты поступления первого и второго сигналов
T = 20  # длительность работы
t = 4  # какая-то переменная
arr = []  # массив успешных координат

for x in range(T):
    for y in range(T):
        if (y < x + t and y > x) or (y > x - t and y < x) or x == y:
            arr.append([x, y])

lines = []

for x in range(0, T):
    line = []
    for y in range(0, T):
        f = 0
        for xy in arr:
            if x == xy[0] and y == xy[1]:
                f = 1
        line.append(f)
    lines.insert(0, line)

for line in lines:
    print(line)