import numpy as np
import scipy.linalg as la

# Матриця коефіцієнтів A та вектор вільних членів B
A = np.array([
    [ 1,  1,  2,  3],
    [ 3, -1, -1, -2],
    [ 2, -3, -1, -1],
    [ 1,  2,  3, -1]
])
b = np.array([1, -4, -6, -4])

# --- 1. Метод Крамера ---[cite: 1]
det_A = np.linalg.det(A)
n = A.shape[0]
x_cramer = np.zeros(n)

if not np.isclose(det_A, 0):
    for i in range(n):
        A_temp = A.copy()
        A_temp[:, i] = b
        x_cramer[i] = np.linalg.det(A_temp) / det_A
    print("Розв'язок методом Крамера:", np.round(x_cramer, 4))
else:
    print("Визначник дорівнює 0, метод Крамера не застосовний.")

# --- 2. Метод оберненої матриці ---[cite: 1]
A_inv = np.linalg.inv(A)
x_inv = A_inv @ b
print("Розв'язок методом оберненої матриці:", np.round(x_inv, 4))

# --- 3. Функція linalg.solve() ---[cite: 1]
x_solve = la.solve(A, b)
print("Розв'язок через linalg.solve():", np.round(x_solve, 4))