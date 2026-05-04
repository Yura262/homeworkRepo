import numpy as np

N = 5  # Розмірність можна змінити

# Створення матриці A та вектора B
A = np.zeros((N, N))
b = np.zeros(N)

for i in range(N):
    b[i] = np.cos(5 * i**2 / np.sqrt(7))**3 #[cite: 1]
    for j in range(N):
        # Використовуємо np.log10 для десяткового логарифма (lg)
        A[i, j] = np.log10((i + j**3 + 1)**(1/5)) #[cite: 1]

# 1. Обчислення виразу: det(A) * A^5 * B - 3 * (A^-1)^3 * B^2[cite: 1]
det_A = np.linalg.det(A)
A_5 = np.linalg.matrix_power(A, 5)
A_inv_3 = np.linalg.matrix_power(np.linalg.inv(A), 3)
B_2 = b**2  # Піднесення вектора до квадрату поелементно

# Матричне множення (@)
result_expr = det_A * (A_5 @ b) - 3 * (A_inv_3 @ B_2)
print("Результат виразу:\n", result_expr)

# 2. Сума елементів останніх чотирьох рядків A і середнє B[cite: 1]
sum_last_4_rows = np.sum(A[-4:, :])
mean_B = np.mean(b)
print(f"\nСума 4 останніх рядків A: {sum_last_4_rows:.4f}")
print(f"Середнє значення B: {mean_B:.4f}")

# 3. Новий вектор C: c_i = b_i + max_j(a_ij) - min_j(a_ij)[cite: 1]
max_A_rows = np.max(A, axis=1)
min_A_rows = np.min(A, axis=1)
c = b + max_A_rows - min_A_rows
print("\nВектор C:\n", c)

# 4. Скалярний добуток векторів B і C[cite: 1]
dot_product = np.dot(b, c)
print(f"\nСкалярний добуток B і C: {dot_product:.4f}")

# 5. Кількість максимальних елементів матриці А[cite: 1]
max_A_val = np.max(A)
count_max_A = np.sum(A == max_A_val)
print(f"\nКількість максимальних елементів в матриці A: {count_max_A}")