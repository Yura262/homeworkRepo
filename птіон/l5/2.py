import numpy as np
import nashpy as nash

# Матриця виграшів цивільних (Civilians)
C = np.array([
    [0, 10],     # Стратегія: Натиснути
    [-10, -100]  # Стратегія: Чекати
])

# Матриця виграшів в'язнів (Prisoners)
P = np.array([
    [0, -10],    # Стратегія: Натиснути
    [10, -100]   # Стратегія: Чекати
])

joker_game = nash.Game(C, P)
equilibria = list(joker_game.support_enumeration())

print("\n--- Завдання 2 (The Dark Knight) ---")
for i, eq in enumerate(equilibria):
    if np.all(np.isin(eq[0], [0, 1])) and np.all(np.isin(eq[1], [0, 1])):
        str1 = "Натиснути" if eq[0][0] == 1 else "Чекати"
        str2 = "Натиснути" if eq[1][0] == 1 else "Чекати"
        print(f"Рівновага Неша #{i+1}: Цивільні - {str1}, В'язні - {str2}")