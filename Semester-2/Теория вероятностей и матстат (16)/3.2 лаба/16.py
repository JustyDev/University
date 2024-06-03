import random
import math
import numpy as np

# Функция для генерации нормального распределения N(2, 4)
def normal(mu, sigma):
    return mu + sigma * math.sqrt(-2 * math.log(random.random())) * math.cos(2 * math.pi * random.random())

# Генерация случайных величин и вычисление z
num_samples = 10000
z_values = []
for _ in range(num_samples):
    x = normal(2, 2)
    y = normal(2, 2)
    z = (y + 2 * x) ** 2
    z_values.append(z)

# Построение гистограммы
histogram_bins = 50
histogram = [0] * histogram_bins
max_z = max(z_values)
bin_width = max_z / histogram_bins

# Подсчет количества значений z в каждом бине
for z in z_values:
    bin_index = int(z // bin_width)
    if bin_index < histogram_bins:
        histogram[bin_index] += 1
    else:
        histogram[histogram_bins - 1] += 1

# Вывод гистограммы
for i in range(histogram_bins):
    print(f'Bin {i+1}: {"*" * (histogram[i] // 50)}')