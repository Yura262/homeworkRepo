import numpy as np
import nashpy as nash

k = 6 # Кількість літер у прізвищі
A = np.array([
    [4, 3, 4, 2],
    [3, 4, 6, 5],
    [2, 5, k, 3]
])

game1 = nash.Game(A)
equilibria = game1.support_enumeration()

print("--- Завдання 1 ---")
for eq in equilibria:
    print(f"Змішана стратегія Г1 (рядки): {np.round(eq[0], 3)}")
    print(f"Змішана стратегія Г2 (стовпці): {np.round(eq[1], 3)}")