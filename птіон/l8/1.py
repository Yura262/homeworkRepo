import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# Дані з умови
temp_max = np.array([17, 19, 21, 28, 33, 38, 37, 37, 31, 23, 19, 18]) #
temp_min = np.array([-62, -59, -56, -46, -32, -18, -9, -13, -25, -46, -52, -58]) #
months = np.arange(1, 13)

# 2. Визначення періодичної функції (період 1 рік = 12 місяців)
# Функція включає середню температуру, амплітуду та зсув за часом
def yearly_temps(times, avg, ampl, time_offset):
    return avg + ampl * np.cos((times + time_offset) * 2 * np.pi / 12)

# 3. Наближення функції до даних
# Підбираємо початкові значення (guess) для кращої збіжності
res_max, _ = optimize.curve_fit(yearly_temps, months, temp_max, p0=[30, 10, 0]) #
res_min, _ = optimize.curve_fit(yearly_temps, months, temp_min, p0=[-30, 20, 0]) #

# Генерація точок для плавного графіка
days = np.linspace(1, 12, 100)

# 1 та 4. Побудова графіків результату
plt.figure(figsize=(10, 6))
plt.plot(months, temp_max, 'ro', label='Max temp (дані)')
plt.plot(days, yearly_temps(days, *res_max), 'r-', label='Max temp (наближення)')

plt.plot(months, temp_min, 'bo', label='Min temp (дані)')
plt.plot(days, yearly_temps(days, *res_min), 'b-', label='Min temp (наближення)')

plt.xlabel('Місяць')
plt.ylabel('Температура (°C)')
plt.title('Температурні екстремуми на Алясці')
plt.legend()
plt.grid(True)
plt.show()

# 5. Аналіз зсуву за часом
print(f"Зсув за часом для Max: {res_max[2]:.2f}")
print(f"Зсув за часом для Min: {res_min[2]:.2f}")