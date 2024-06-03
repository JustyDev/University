import random

# Количество случайных значений
num_samples = 10000

# Генерация случайных чисел x и y с нормальным распределением N(2, 4)
mean = 2
std_dev = 2  # Отклонение равно корню от дисперсии (т.е. корень от 4)

x_values = [random.gauss(mean, std_dev) for _ in range(num_samples)]
y_values = [random.gauss(mean, std_dev) for _ in range(num_samples)]

# Вычисление z = (y + 2x)^2
z_values = [(y + 2 * x) ** 2 for x, y in zip(x_values, y_values)]

# Построение гистограммы
# Определяем количество бинов
num_bins = 50
min_z = min(z_values)
max_z = max(z_values)
bin_width = (max_z - min_z) / num_bins

# Подсчет частот для каждого бина
histogram = [0] * num_bins
for z in z_values:
    bin_index = int((z - min_z) / bin_width)
    if bin_index == num_bins:  # В случае, если значение z попадает в последний бин
        bin_index -= 1
    histogram[bin_index] += 1

# Вывод результатов
for i in range(num_bins):
    bin_start = min_z + i * bin_width
    bin_end = bin_start + bin_width
    print(f"{(i + 1):>3.0f} ({bin_start:>7.2f}, {bin_end:>7.2f}): {'*' * int(histogram[i] / histogram[0] * 100)} ({histogram[i]})")
