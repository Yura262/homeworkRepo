import numpy as np
import nashpy as nash
import requests

def get_weather_probability(api_key, city="Kyiv"):
    """
    Отримання ймовірності опадів через OpenWeatherMap API.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Перевіряємо наявність дощу або снігу
        if 'rain' in data or 'snow' in data:
            return 0.8 # Висока ймовірність поганої погоди
        elif 'clouds' in data and data['clouds']['all'] > 80:
            return 0.4 # Середня ймовірність
        else:
            return 0.1 # Низька ймовірність
    except:
        # У разі відсутності ключа повертаємо тестове значення
        print("API недоступний або ключ недійсний. Використовуємо тестове значення ймовірності опадів: 60%")
        return 0.6 

# 1. Отримуємо прогноз погоди (тут вставте свій ключ OpenWeatherMap)
API_KEY = "YOUR_API_KEY_HERE"
bad_weather_prob = get_weather_probability(API_KEY)

# 2. Встановлюємо виграші (Payoffs)
# Стратегії: [Доставляти (Ризик), Чекати]
# Уявімо, що базовий дохід = 10, втрата доходу = 0, втрати від аварії = -15

# Обчислюємо очікуваний виграш, якщо обидва ризикують
# Якщо погода хороша (1 - bad_weather_prob), обидва заробляють по 5
# Якщо погода погана (bad_weather_prob), обидва втрачають -15
expected_risk_payoff = (5 * (1 - bad_weather_prob)) + (-15 * bad_weather_prob)

# Матриця виграшів для Складу 1 (Рядки) та Складу 2 (Стовпці)
# [Доставляти, Доставляти] | [Доставляти, Чекати]
# [Чекати, Доставляти]     | [Чекати, Чекати]

# Формуємо матриці виграшів
warehouse_1_matrix = np.array([
    [expected_risk_payoff, 10],  # Склад 1 доставляє
    [-2, 0]                      # Склад 1 чекає (-2 це втрата частки ринку)
])

warehouse_2_matrix = np.array([
    [expected_risk_payoff, -2],  # Склад 2 доставляє (читається по стовпцях)
    [10, 0]                      # Склад 2 чекає
])

# 3. Створення гри та пошук рівноваги Неша
delivery_game = nash.Game(warehouse_1_matrix, warehouse_2_matrix)
equilibria = list(delivery_game.support_enumeration())

print(f"\n--- Аналіз Гри ---")
print(f"Імовірність поганої погоди: {bad_weather_prob*100}%")
print(f"Матриця виграшів Складу 1:\n{warehouse_1_matrix}")
print(f"Матриця виграшів Складу 2:\n{warehouse_2_matrix}")

print("\n--- Рівноваги Неша ---")
for i, eq in enumerate(equilibria):
    p1_strategy, p2_strategy = eq
    print(f"Рівновага {i+1}:")
    print(f"Склад 1 (Доставляти, Чекати): {p1_strategy}")
    print(f"Склад 2 (Доставляти, Чекати): {p2_strategy}")