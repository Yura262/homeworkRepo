

# t=[1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985]
# y=[14.1,9.3,19.4,19.7,5.4,24.2,13.8,21.5,14.7,16.6,5.6,16.2,25.3,11.9,18.5]


# 1. Дослідити даний Вам часовий ряд (результати спостережень) на наявність у ньому
# тренду (закономірності).
# 2. Побудувати тренд даного Вам ряду методами згладжування.
# 3. Побудувати тренд даного Вам ряду у вигляді відповідного многочлена.








# print("--- 1. ДОСЛІДЖЕННЯ НА НАЯВНІСТЬ ТРЕНДУ ---")

# # 1. Розбиваємо ряд приблизно навпіл
# mid = len(y) // 2
# y1, y2 = y[:mid], y[mid:]
# print(f"Перша половина: {y1}\nДруга половина: {y2}\n")
# # 2. Обчислюємо незміщені вибіркові дисперсії (ddof=1)
# var_y1 = np.var(y1, ddof=0)
# var_y2 = np.var(y2, ddof=0)

# print(f"Дисперсія першої половини: {var_y1:.4f}",
#       f"\nДисперсія другої половини: {var_y2:.4f}")


# print("Середнє першої половини",np.average(y1), "\nСереднє другої половини",np.average(y2))
# var_y1 = 36.08
# var_y2 = 36.15

# print("\n")


# # 3. Перевірка рівності дисперсій (Критерій Фішера)
# f_stat = var_y2 / var_y1 if var_y2 > var_y1 else var_y1 / var_y2
# df1 = len(y2) - 1 if var_y2 > var_y1 else len(y1) - 1
# df2 = len(y1) - 1 if var_y2 > var_y1 else len(y2) - 1
# p_value_f = 1 - stats.f.cdf(f_stat, df1, df2)

# print(f"Критерій Фішера (дисперсії): F = {f_stat:.4f}, p-value = {p_value_f:.4f}")

# # 4. Перевірка рівності середніх (Критерій Стьюдента)
# # equal_var=True використовується, бо критерій Фішера не відкинув рівність дисперсій
# t_stat, p_value_t = stats.ttest_ind(y1, y2, equal_var=True)
# print(f"Критерій Стьюдента (середні): t = {t_stat:.4f}, p-value = {p_value_t:.4f}")

# if p_value_t > 0.05:
#     print("Висновок: Статистично значущого тренду немає (p-value > 0.05).\n")
# else:
#     print("Висновок: Ряд має статистично значущий тренд.\n")

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

t=[1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
#1<=t<=3
y=[-0.814956, 0.150201, 3.17186, 3.38067, -1.51027, 2.0845, 1.89613, 3.64936, 2.84892,
3.9241, -0.583957, 2.85666, 5.68384, -1.01523, 5.37776, 1.97718, -1.22311, 4.71863, 5.72951, -
0.327803, 3.90939]



n = len(y)
n1, n2 = n // 2, n - (n // 2) # n1=10, n2=11
y1, y2 = y[:n1], y[n1:]

mean1, mean2 = np.mean(y1), np.mean(y2)
var1, var2 = np.var(y1, ddof=1), np.var(y2, ddof=1)

# Критерій Фішера 
F_emp = max(var1, var2) / min(var1, var2)
df_num = n2 - 1 if var2 > var1 else n1 - 1
df_den = n1 - 1 if var2 > var1 else n2 - 1
F_crit = stats.f.ppf(1 - 0.05, df_num, df_den) # alpha = 0.05

# Критерій Стьюдента 
num = mean1 - mean2
denom = np.sqrt((n1 - 1) * var1 + (n2 - 1) * var2)
mult = np.sqrt((n1 * n2 * (n1 + n2 - 2)) / (n1 + n2))
t_emp = (num / denom) * mult
t_crit = stats.t.ppf(1 - 0.025, n1 + n2 - 2) 

print(f"Критерій Фішера: F_emp = {F_emp:.4f}, F_crit = {F_crit:.4f}")
print(f"Критерій Стьюдента: t_emp = {t_emp:.4f}, t_crit = {t_crit:.4f}")


sma = np.copy(y)
sma[0] = np.mean(y[0:2]) 
for i in range(1, n-1):
    sma[i] = np.mean(y[i-1:i+2])
sma[-1] = np.mean(y[-2:]) 

n_ema = 3
ema = np.zeros(n)
ema[0] = y[0]
for i in range(1, n):
    ema[i] = (ema[i-1] * (n_ema - 1) + 2 * y[i]) / (n_ema + 1)

plt.figure(figsize=(10, 6))
plt.plot(t, y, marker='o', linestyle='-', label='Початковий ряд (Спостереження)', color='gray', alpha=0.5)
plt.plot(t, sma, marker='s', linestyle='--', label='Ковзаюче середнє (SMA, n=3)', color='blue')
plt.plot(t, ema, marker='^', linestyle='-.', label='Експонентне середнє (EMA, n=3)', color='green')

plt.title('Часовий ряд та виділення тренду методами згладжування')
plt.xlabel('Час (t)')
plt.ylabel('Значення (y)')
plt.legend()
plt.grid(True)
plt.show()




print("Аналіз скінченних різниць:")
diff_1 = np.diff(y)       
print(f"Перші скінченні різниці: {diff_1}")
diff_2 = np.diff(diff_1)   
print(f"Другі скінченні різниці: {diff_2}")
diff_3 = np.diff(diff_2)   
print(f"Треті скінченні різниці: {diff_3}")


std_1 = np.std(diff_1)
std_2 = np.std(diff_2)
std_3 = np.std(diff_3)

print(f"Стандартне відхилення перших різниць: {std_1:.4f}")
print(f"Стандартне відхилення других різниць: {std_2:.4f}")
print(f"Стандартне відхилення третіх різниць: {std_3:.4f}")


coeffs_linear = np.polyfit(t, y, 1)
trend_linear = np.polyval(coeffs_linear, t)
print(f"\nРівняння лінійного тренду: y(t) = {coeffs_linear[0]:.4f}*t + {coeffs_linear[1]:.4f}")

coeffs_quad = np.polyfit(t, y, 2)
trend_quad = np.polyval(coeffs_quad, t)
print(f"Рівняння квадратичного тренду: y(t) = {coeffs_quad[0]:.4f}*t^2 + {coeffs_quad[1]:.4f}*t + {coeffs_quad[2]:.4f}")

plt.figure(figsize=(10, 6))
plt.plot(t, y, marker='o', linestyle='-', label='Фактичні дані $y_t$', color='gray', alpha=0.6)
plt.plot(t, trend_linear, linestyle='--', color='blue', linewidth=2, 
         label=f'Лінійний тренд (m=1)')
plt.plot(t, trend_quad, linestyle='-', color='red', linewidth=2, 
         label=f'Квадратичний тренд (m=2)')

plt.title('Побудова многочленного тренду')
plt.xlabel('Час (t)')
plt.ylabel('Значення (y)')
plt.legend()
plt.grid(True)
plt.show()