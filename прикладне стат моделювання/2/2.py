import numpy as np

def integrand(x):
    """Підінтегральна функція f(x)"""
    return 1 / (x**2 - 3*x + 2)

def monte_carlo_uniform(N):
    """Варіант 1: Використання рівномірного розподілу на [3, 4]"""
    # Генеруємо N випадкових чисел з рівномірним розподілом U(3, 4)
    xi = np.random.uniform(3, 4, N)
    
    # Оскільки p(x) = 1, оцінка є просто середнім значенням f(xi)
    integral_estimate = np.mean(integrand(xi))
    return integral_estimate

def monte_carlo_linear(N):
    """Варіант 2: Використання лінійного розподілу p(x) = 2(x-3)"""
    # Генеруємо базові рівномірні числа gamma на [0, 1]
    gamma = np.random.uniform(0, 1, N)
    
    # Застосовуємо метод обернених функцій для отримання нашого розподілу
    eta = 3 + np.sqrt(gamma)
    
    # Обчислюємо щільність у згенерованих точках: p(eta) = 2 * (eta - 3)
    p_eta = 2 * (eta - 3)
    
    # Оцінка: середнє значення f(eta) / p(eta)
    integral_estimate = np.mean(integrand(eta) / p_eta)
    return integral_estimate

if __name__ == "__main__":
    # Кількість статистичних випробувань
    N_trials = 1_000_000 
    
    # Точне аналітичне значення для порівняння
    exact_value = 2 * np.log(2) - np.log(3)
    
    # Запуск симуляцій
    est_uniform = monte_carlo_uniform(N_trials)
    est_linear = monte_carlo_linear(N_trials)
    
    # Виведення результатів
    print(f"Точне аналітичне значення: {exact_value:.6f}")
    print("-" * 50)
    print(f"Оцінка (рівномірний розп.): {est_uniform:.6f}")
    print(f"Абсолютна похибка:         {abs(exact_value - est_uniform):.6f}")
    print("-" * 50)
    print(f"Оцінка (лінійний розп.):   {est_linear:.6f}")
    print(f"Абсолютна похибка:         {abs(exact_value - est_linear):.6f}")