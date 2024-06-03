import math
import numpy as np
from scipy.stats import t, chi2, skew, kurtosis

data = [
    13.870, 8.929, 14.845, 13.813, 11.779,
    13.226, 7.986, 6.004, 11.242, 14.091,
    5.535, 9.195, 5.347, 7.172, 10.827,
    7.548, 14.110, 9.906, 14.095, 7.726
]

# Шаг 1: Преобразование выборки в вариационный ряд
sorted_data = sorted(data)
print("Вариационный ряд:", sorted_data)

# Шаг 2: Вычисление точечных оценок
n = len(data)
mean = np.mean(data)
variance = np.var(data, ddof=1)
std_dev = np.std(data, ddof=1)
coefficient_of_variation = std_dev / mean

print(f"МО (математическое ожидание): {mean}")
print(f"Дисперсия: {variance}")
print(f"СКО (среднеквадратическое отклонение): {std_dev}")
print(f"Коэффициент вариации: {coefficient_of_variation}")
print(f"Коэффициент асимметрии: {skew(data, bias=False)}")
print(f"Коэффициент эксцесса: {kurtosis(data, bias=False)}")
print(f"Медиана: {np.median(sorted_data)}")
print(f"Размах: {max(data) - min(data)}")

# Шаг 5: Построение интервальных оценок для МО и дисперсии
gamma = 0.95
alpha = 1 - gamma
t_critical = t.ppf(1 - alpha / 2, n - 1)
mean_conf_interval = (mean - t_critical * std_dev / math.sqrt(n), mean + t_critical * std_dev / math.sqrt(n))

chi2_lower = chi2.ppf(alpha / 2, n - 1)
chi2_upper = chi2.ppf(1 - alpha / 2, n - 1)
variance_conf_interval = ((n - 1) * variance / chi2_upper, (n - 1) * variance / chi2_lower)

print(f"Интервальная оценка для МО: {mean_conf_interval}")
print(f"Интервальная оценка для дисперсии: {variance_conf_interval}")
