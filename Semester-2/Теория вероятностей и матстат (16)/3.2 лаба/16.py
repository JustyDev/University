import numpy as np

# Параметры распределения
mean = 2
std_dev = 2

# Количество выборок
num_samples = 10000

# Генерация нормальных случайных величин x и y
x = np.random.normal(mean, std_dev, num_samples)
y = np.random.normal(mean, std_dev, num_samples)

# Вычисление величины z
z = (y + 2 * x) ** 2

# Создание гистограммы
hist, bin_edges = np.histogram(z, bins=50)

# Нормализация гистограммы
hist = hist / np.sum(hist)


# Функция для вывода гистограммы в консоли
def print_histogram(hist, bin_edges, max_width=100):
    max_height = np.max(hist)
    scaling_factor = max_width / max_height

    for i in range(len(hist)):
        bar = '*' * int(hist[i] * scaling_factor)
        print(f'{bin_edges[i]:.2f} - {bin_edges[i + 1]:.2f}: {bar} ({hist[i]:.4f})')


# Вывод гистограммы в консоли
print_histogram(hist, bin_edges)