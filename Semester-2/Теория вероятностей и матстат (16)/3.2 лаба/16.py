import numpy as np
import matplotlib.pyplot as plt

# Задаем параметры распределения
mu = 2
sigma = 2

# Размер выборки
sample_size = 10000

# Генерация выборок случайных величин x и y
x = np.random.normal(mu, sigma, sample_size)
y = np.random.normal(mu, sigma, sample_size)

# Вычисление z = (y + 2x)^2
z = (y + 2 * x) ** 2

# Построение гистограммы
plt.hist(z, bins=100, density=True, alpha=0.6, color='g')

# Добавление заголовка и меток осей
plt.title('Гистограмма распределения случайной величины z = (y + 2x)^2')
plt.xlabel('Значение z')
plt.ylabel('Плотность вероятности')

# Показ гистограммы
plt.show()