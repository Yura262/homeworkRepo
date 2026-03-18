import numpy as np
import random
def generateRandomNumbers(n):
    numbers = []
    for i in range(n):
        numbers.append(random.random())
    return np.array(numbers)

def func(x):
    return 1 / (x**2 - 3*x + 2)

def uniform(N):
    gamma = generateRandomNumbers(N)
    const = 0.4
    integral_estimate = np.mean(const * func(const * gamma))
    return integral_estimate

def hyperb(N):
    gamma = generateRandomNumbers(N)

    eta = 12/(4-gamma)
    
    p_eta = 12/eta**2
    
    integral_estimate = np.mean(func(eta) / p_eta)
    return integral_estimate

if __name__ == "__main__":
    N_trials = 1000
    
    exact_value = 2 * np.log(2) - np.log(3)
        
    est_uniform = uniform(N_trials)
    est_linear = hyperb(N_trials)
    
    
    print(f"Точне аналітичне значення: {exact_value:.6f}")
    print("-" * 50)
    print(f"Оцінка (рівномірний розп.): {est_uniform:.6f}")
    print(f"Абсолютна похибка:         {abs(exact_value - est_uniform):.6f}")
    print("-" * 50)
    print(f"Оцінка (гіперболічний розп.):   {est_linear:.6f}")
    print(f"Абсолютна похибка:         {abs(exact_value - est_linear):.6f}")
    





# import numpy as np
# import math

# def func(x):
    
#     return np.sin(x)

# def uniform(N):
#     psi = np.array([0.865,0.159,0.079,0.566,0.155,0.664,0.345,0.655,0.812,0.332])
#     #np.random.uniform(0, 1, N)
#     const = math.pi/2
#     print("gamma",psi)
#     print("psi",const*psi)
#     print("sin",func(const *psi))
#     print("sum/10",sum(const*func(const*psi))/10)
#     integral_estimate = np.mean( func(const *psi))
#     return integral_estimate

# def linear(N):
#     gamma = np.random.uniform(0, 1, N)
        
#     eta = 3 + np.sqrt(gamma)
        
#     p_eta = 2 * (eta - 3)
    
#     integral_estimate = np.mean(func(eta) / p_eta)
#     return integral_estimate

# if __name__ == "__main__":
#     while True:
#         N_trials = 10
        
#         exact_value = 1
            
#         est_uniform = uniform(N_trials)
#         print(est_uniform)
#         est_linear = linear(N_trials)
#         print("lin",est_linear)
        
        
#         print(f"Точне аналітичне значення: {exact_value:.6f}")
#         print("-" * 50)
#         print(f"Оцінка (рівномірний розп.): {est_uniform:.6f}")
#         print(f"Абсолютна похибка:         {abs(exact_value - est_uniform):.6f}")
#         print("-" * 50)
#         print(f"Оцінка (лінійний розп.):   {est_linear:.6f}")
#         print(f"Абсолютна похибка:         {abs(exact_value - est_linear):.6f}")
#         input()