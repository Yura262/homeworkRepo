import numpy as np
import random

import secrets


def generateRandomNumbers(n):
    numbers = []
    for i in range(n):
        numbers.append(random.random())
    return np.array(numbers)

def generateRandomNumbersT(n):
    numbers = []
    for i in range(n):
        numbers.append(secrets.SystemRandom().random())
    return np.array(numbers)



def func(x):
    return 1 / (x**2 - 3*x + 2)

def uniformT(N):
    gamma = generateRandomNumbersT(N)
    const = 0.4
    integral_estimate = np.mean(const * func(const * gamma))
    return integral_estimate

def hyperbT(N):
    gamma = generateRandomNumbersT(N)

    eta = 12/(4-gamma)
    
    p_eta = 12/eta**2
    
    integral_estimate = np.mean(func(eta) / p_eta)
    return integral_estimate



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
    avgHyperb = None
    avgLinear = None
    AvgValCount=0
    for i in range(5000):
        est_uniform = uniform(N_trials)
        est_linear = hyperb(N_trials)
        AvgValCount += 1
        avgLinear = est_linear if avgLinear is None else (avgLinear +(est_linear-avgLinear)/AvgValCount)
        avgHyperb = est_uniform if avgHyperb is None else (avgHyperb +(est_uniform-avgHyperb)/AvgValCount)
        
    avgHyperbT = None
    avgLinearT = None
    AvgValCountT=0
    for i in range(5000):
        est_uniform = uniformT(N_trials)
        est_linear = hyperbT(N_trials)
        AvgValCountT += 1
        avgLinearT = est_linear if avgLinearT is None else (avgLinearT +(est_linear-avgLinearT)/AvgValCountT)
        avgHyperbT = est_uniform if avgHyperbT is None else (avgHyperbT +(est_uniform-avgHyperbT)/AvgValCountT)
            
        
    print(f"Оцінка (рівномірний розп.): {abs(exact_value-avgLinear)}")
    print(f"Оцінка (гіперболічний розп.):   {abs(exact_value-avgHyperb)}")
    
    print(f"Оцінка (рівномірний розп.): {abs(exact_value-avgLinearT)}")
    print(f"Оцінка (гіперболічний розп.):   {abs(exact_value-avgHyperbT)}")

