import numpy as np
import matplotlib.pyplot as plt

# 1. Вхідні дані та налаштування сітки
step = 0.01
x1_vals = np.arange(-2, 2 + step, step)
x2_vals = np.arange(-2, 2 + step, step)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# 2. Цільові функції
F1 = 6*X1**2 - 12*X1 + 4*X2**2 + 8*X2 + 40
F2 = -8*X1**2 + 16*X1 - 3*X2**2 + 6*X2 + 50

# 3. Табличний метод: пошук гарантованих результатів (Вальд)
# Суб'єкт 1 контролює x1 (стовпці в meshgrid, якщо x2 - рядки).
# Очікує мінімуму від x2 (по осі 0 - по рядках).
min_x2_F1 = np.min(F1, axis=0)
f1_star = np.max(min_x2_F1)
x1_guaranteed_idx = np.argmax(min_x2_F1)
x1_guaranteed = x1_vals[x1_guaranteed_idx]

# Суб'єкт 2 контролює x2 (рядки). Очікує мінімуму від x1 (по осі 1 - по стовпцях).
min_x1_F2 = np.min(F2, axis=1)
f2_star = np.max(min_x1_F2)
x2_guaranteed_idx = np.argmax(min_x1_F2)
x2_guaranteed = x2_vals[x2_guaranteed_idx]

print("--- Гарантовані результати ---")
print(f"f1* = {f1_star:.4f} (при x1 = {x1_guaranteed:.2f})")
print(f"f2* = {f2_star:.4f} (при x2 = {x2_guaranteed:.2f})")

# 4. Пошук множини Парето з урахуванням технічних обмежень
# Умова: f1 >= f1* та f2 >= f2*
valid_mask = (F1 >= f1_star) & (F2 >= f2_star)

valid_x1 = X1[valid_mask]
valid_x2 = X2[valid_mask]
valid_f1 = F1[valid_mask]
valid_f2 = F2[valid_mask]

# Спрощений пошук недомінованих точок (максимізація обох)
is_pareto = np.ones(len(valid_f1), dtype=bool)
for i in range(len(valid_f1)):
    # Точка домінується, якщо є інша точка, де обидві функції не менші, і хоча б одна більша
    if is_pareto[i]:
        dominated = np.any((valid_f1 >= valid_f1[i]) & (valid_f2 >= valid_f2[i]) & 
                           ((valid_f1 > valid_f1[i]) | (valid_f2 > valid_f2[i])))
        if dominated:
            is_pareto[i] = False

pareto_x1 = valid_x1[is_pareto]
pareto_x2 = valid_x2[is_pareto]
pareto_f1 = valid_f1[is_pareto]
pareto_f2 = valid_f2[is_pareto]

# 5. Пошук оптимальних значень x1*, x2* (Мінімізація Дельта)
# Формуємо "Утопічну" точку (ідеальні максимальні значення в множині Парето)
f1_ideal = np.max(pareto_f1)
f2_ideal = np.max(pareto_f2)

# Шукаємо точку, яка мінімізує відстань до ідеалу (компроміс)
# Нормуємо функції для коректного обчислення відстані, або обчислюємо пряму дельту
deltas = np.sqrt((pareto_f1 - f1_ideal)**2 + (pareto_f2 - f2_ideal)**2)
opt_idx = np.argmin(deltas)

opt_x1 = pareto_x1[opt_idx]
opt_x2 = pareto_x2[opt_idx]
opt_f1 = pareto_f1[opt_idx]
opt_f2 = pareto_f2[opt_idx]

print("\n--- Оптимальне компромісне рішення (Мінімізація Дельта) ---")
print(f"x1* = {opt_x1:.4f}, x2* = {opt_x2:.4f}")
print(f"f1(x1*, x2*) = {opt_f1:.4f}")
print(f"f2(x1*, x2*) = {opt_f2:.4f}")

# 6. Графічний метод
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Простір критеріїв
ax1.scatter(F1.flatten()[::100], F2.flatten()[::100], c='lightgray', s=5, label='Всі точки (проріджено)')
ax1.scatter(valid_f1, valid_f2, c='blue', s=10, alpha=0.5, label='Задовольняють f>=f*')
ax1.scatter(pareto_f1, pareto_f2, c='red', s=20, label='Множина Парето')
ax1.scatter(opt_f1, opt_f2, c='green', s=100, marker='*', zorder=5, label='Оптимальна точка')

ax1.axvline(x=f1_star, color='k', linestyle='--', label=f'f1* = {f1_star}')
ax1.axhline(y=f2_star, color='k', linestyle=':', label=f'f2* = {f2_star}')
ax1.set_xlabel('f1')
ax1.set_ylabel('f2')
ax1.set_title('Простір критеріїв')
ax1.legend()
ax1.grid(True)

# Простір рішень (x1, x2)
ax2.scatter(X1.flatten()[::100], X2.flatten()[::100], c='lightgray', s=5)
ax2.scatter(valid_x1, valid_x2, c='blue', s=10, alpha=0.5, label='Допустимі X')
ax2.scatter(pareto_x1, pareto_x2, c='red', s=20, label='X для Парето')
ax2.scatter(opt_x1, opt_x2, c='green', s=100, marker='*', zorder=5, label='Оптимальні x1*, x2*')

ax2.set_xlabel('x1')
ax2.set_ylabel('x2')
ax2.set_title('Простір рішень (змінних)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()