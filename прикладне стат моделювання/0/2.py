import numpy as np

def integrand(x):
    return 1 / (x**2 - 3*x + 2)

def uniform(N):
    psi = np.random.uniform(0, 1, N)
    const = 0.3
    integral_estimate = np.mean(const * integrand(psi))
    return integral_estimate

def linear(N):
    gamma = np.random.uniform(0, 1, N)
        
    eta = 3 + np.sqrt(gamma)
        
    p_eta = 2 * (eta - 3)
    
    integral_estimate = np.mean(integrand(eta) / p_eta)
    return integral_estimate

if __name__ == "__main__":
    N_trials = 100
    
    exact_value = 2 * np.log(2) - np.log(3)
        
    est_uniform = uniform(N_trials)
    est_linear = linear(N_trials)
    
    
    print(f"Точне аналітичне значення: {exact_value:.6f}")
    print("-" * 50)
    print(f"Оцінка (рівномірний розп.): {est_uniform:.6f}")
    print(f"Абсолютна похибка:         {abs(exact_value - est_uniform):.6f}")
    print("-" * 50)
    print(f"Оцінка (лінійний розп.):   {est_linear:.6f}")
    print(f"Абсолютна похибка:         {abs(exact_value - est_linear):.6f}")
    input()