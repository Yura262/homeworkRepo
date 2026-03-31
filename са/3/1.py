# import pandas as pd
# import numpy as np

# # 1. Зчитування даних
# df_X = pd.read_csv('Xi_1.csv')
# df_Y = pd.read_csv('Yi_1.csv')

# # Виділення факторів (матриця А) та цільових значень
# A = df_X[['X11', 'X12', 'X21', 'X22', 'X31', 'X32', 'X33']].values
# Y_data = df_Y[['Y1', 'Y2', 'Y3', 'Y4']].values

# # 2. Метод статистичного градієнта
# def solve_sgd(A, Y_target, epochs=1000000, lr_init=1e-4):
#     num_vars = A.shape[1]
#     num_samples = A.shape[0]
#     C = np.zeros(num_vars) 
    
#     # Випадковий вибір індексів рівнянь для стохастичності
#     np.random.seed(42)
#     indices = np.random.randint(0, num_samples, epochs)
    
#     for t in range(epochs):
#         # Зменшення кроку навчання з часом (Learning rate decay)
#         lr = lr_init / (1 + 1e-5 * t)
        
#         p = indices[t]      # випадковий дослід
#         A_p = A[p]          # параметри p-го досліду
#         Y_p = Y_target[p]   # цільове значення p-го досліду
        
#         # Обчислення прогнозу і похибки
#         prediction = np.dot(A_p, C)
#         error = prediction - Y_p
        
#         # Оновлення вектора коефіцієнтів
#         C -= lr * error * A_p
        
#     return C

# # 3. Розв'язання для кожної з 4-х функцій
# for i in range(4):
#     Y_i = Y_data[:, i]
    
#     # Знаходження b_iq0
#     b_iq0 = (np.max(Y_i) + np.min(Y_i)) / 2.0
    
#     # Центрування
#     Y_i_centered = Y_i - b_iq0
    
#     # Запуск оптимізації
#     C_sgd = solve_sgd(A, Y_i_centered, epochs=1000000, lr_init=1e-4)
    
#     # Виведення
#     print(f"--- Результати для Y{i+1} ---")
#     print(f"b_iq0 = {b_iq0:.2f}")
#     print("Коефіцієнти [C11, C12, C21, C22, C31, C32, C33]:")
#     print(np.round(C_sgd, 2))
#     print()






import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Зчитування даних
df_X = pd.read_csv('Xi_1.csv')
df_Y = pd.read_csv('Yi_1.csv')

# Виділення факторів (матриця А) та цільових значень
A = df_X[['X11', 'X12', 'X21', 'X22', 'X31', 'X32', 'X33']].values
Y_data = df_Y[['Y1', 'Y2', 'Y3', 'Y4']].values
q0_vals = df_Y['q0'].values # Для осі X на графіках

# 2. Метод статистичного градієнта
def solve_sgd(A, Y_target, epochs=1000000, lr_init=1e-4):
    num_vars = A.shape[1]
    num_samples = A.shape[0]
    C = np.zeros(num_vars) 
    
    # Випадковий вибір індексів рівнянь для стохастичності
    np.random.seed(42)
    indices = np.random.randint(0, num_samples, epochs)
    
    for t in range(epochs):
        # Зменшення кроку навчання з часом (Learning rate decay)
        lr = lr_init / (1 + 1e-5 * t)
        
        p = indices[t]      # випадковий дослід
        A_p = A[p]          # параметри p-го досліду
        Y_p = Y_target[p]   # цільове значення p-го досліду
        
        # Обчислення прогнозу і похибки
        prediction = np.dot(A_p, C)
        error = prediction - Y_p
        
        # Оновлення вектора коефіцієнтів
        C -= lr * error * A_p
        
    return C

# --- ДОДАНО БЛОК UI ---
# Створюємо фігуру для 4 графіків (2 рядки, 2 стовпці)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

# 3. Розв'язання для кожної з 4-х функцій та побудова UI
for i in range(4):
    Y_i = Y_data[:, i]
    
    # Знаходження b_iq0
    b_iq0 = (np.max(Y_i) + np.min(Y_i)) / 2.0
    
    # Центрування
    Y_i_centered = Y_i - b_iq0
    
    # Запуск оптимізації методом SGD
    C_sgd = solve_sgd(A, Y_i_centered, epochs=1000000, lr_init=1e-4)
    
    # Виведення в консоль
    print(f"--- Результати для Y{i+1} ---")
    print(f"b_iq0 = {b_iq0:.2f}")
    print("Коефіцієнти [C11, C12, C21, C22, C31, C32, C33]:")
    print(np.round(C_sgd, 2))
    print()

    # --- ДОДАНО БЛОК МАЛЮВАННЯ ГРАФІКІВ ---
    # Обчислюємо прогнозовані значення, використовуючи коефіцієнти C_sgd
    Y_pred_sgd = np.dot(A, C_sgd) + b_iq0
    
    ax = axes[i]
    # Малюємо фактичні значення
    ax.plot(q0_vals, Y_i, label='Фактичні (Actual)', marker='o', linestyle='-', color='blue')
    # Малюємо прогноз, знайдений вашим алгоритмом
    ax.plot(q0_vals, Y_pred_sgd, label='Прогноз SGD (Predicted)', marker='x', linestyle='--', color='green')
    
    # Налаштування вигляду графіка
    ax.set_title(f'Функція Y{i+1} (Метод SGD)', fontsize=12)
    ax.set_xlabel('Номер досліду (q0)', fontsize=10)
    ax.set_ylabel(f'Значення Y{i+1}', fontsize=10)
    ax.legend()
    ax.grid(True, alpha=0.5)

# Зберігаємо UI як картинку
plt.tight_layout()
plt.savefig('sgd_ui_plots.png', dpi=300)