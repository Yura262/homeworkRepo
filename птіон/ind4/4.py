import numpy as np
import math
from scipy.special import ellipkinc, ellipeinc
import scipy.integrate as integrate
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

print("="*50)
print("ЗАВДАННЯ 1: Площа поверхні еліпсоїда")
print("="*50)

def ellipsoid_surface_exact(a, b, c):
    """Обчислення точної площі через неповні еліптичні інтеграли"""
    # Сортуємо півосі, щоб a >= b >= c
    a, b, c = sorted([a, b, c], reverse=True)
    
    if a == c: # Якщо це сфера
        return 4 * np.pi * a**2

    phi = math.acos(c / a)
    sin_phi = math.sin(phi)
    cos_phi = math.cos(phi)

    # Параметр m = k^2
    k_sq = (a**2 * (b**2 - c**2)) / (b**2 * (a**2 - c**2))

    # ellipkinc - неповний еліптичний інтеграл першого роду (F)
    # ellipeinc - неповний еліптичний інтеграл другого роду (E)
    # У scipy другим аргументом передається саме m = k^2
    F = ellipkinc(phi, k_sq) 
    E = ellipeinc(phi, k_sq)

    S = 2 * np.pi * c**2 + (2 * np.pi * a * b / sin_phi) * (F * cos_phi**2 + E * sin_phi**2)
    return S

def ellipsoid_surface_approx(a, b, c):
    """Обчислення за наближеною формулою з умови"""
    a, b, c = sorted([a, b, c], reverse=True)
    
    if a == c:
        return 4 * np.pi * a**2

    phi = math.acos(c / a)
    sin_phi = math.sin(phi)

    term1 = 2 * np.pi * c**2
    term2_inner = 1 - ((3*b**2 + 10*c**2) / (56*b**2)) * (phi**2 / sin_phi**2)
    term2_outer = 1 - ((b**2 - c**2) / (6*b**2)) * term2_inner
    term2 = 2 * np.pi * a * b * term2_outer

    return term1 + term2

# Тестування для еліпсоїдів різних форм
test_shapes = [
    (5.0, 4.0, 3.0),
    (10.0, 8.0, 1.0),
    (7.0, 7.0, 2.0)
]

for a, b, c in test_shapes:
    exact_S = ellipsoid_surface_exact(a, b, c)
    approx_S = ellipsoid_surface_approx(a, b, c)
    print(f"Півосі (a={a}, b={b}, c={c}):")
    print(f"  Точна площа:     {exact_S:.6f}")
    print(f"  Наближена площа: {approx_S:.6f}")
    print(f"  Абсолютна різниця: {abs(exact_S - approx_S):.6f}\n")


print("="*50)
print("ЗАВДАННЯ 2: Обчислення інтегралу")
print("="*50)

# Підінтегральна функція. x^(-x) має невизначеність у нулі, 
# але границя при x -> 0 дорівнює 1.
def f(x):
    if x == 0:
        return 1.0
    return x**(-x)

# Обчислення через scipy.integrate.quad
integral_val, error = integrate.quad(f, 0, 1)

# Обчислення суми ряду (беремо 20 членів, цього достатньо для високої точності)
series_sum = sum(n**(-n) for n in range(1, 25))

print(f"Значення інтеграла (quad): {integral_val:.10f}")
print(f"Оцінка похибки:            {error:.2e}")
print(f"Сума ряду (n=1..25):       {series_sum:.10f}")
print(f"Різниця:                   {abs(integral_val - series_sum):.10e}\n")


print("="*50)
print("ЗАВДАННЯ 3: Класифікація пухлин та ROC-крива")
print("="*50)

# 1. Завантаження даних
data = load_breast_cancer()
X = data.data
y = data.target
feature_names = data.feature_names

# Розбиття на тренувальну та тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. Навчання моделі RandomForest
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train, y_train)

# 3. Важливість ознак
importances = rf_clf.feature_importances_
# Сортуємо ознаки за важливістю для виводу
indices = np.argsort(importances)[::-1]

print("Топ-5 найважливіших ознак клітин:")
for i in range(5):
    print(f"  {i+1}. {feature_names[indices[i]]} (вага: {importances[indices[i]]:.4f})")

# 4. Побудова ROC-кривої
# Отримуємо ймовірності приналежності до позитивного класу
y_prob = rf_clf.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

# Візуалізація
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC-крива (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (Хибно-позитивні)')
plt.ylabel('True Positive Rate (Істинно-позитивні)')
plt.title('ROC-крива (Random Forest, Breast Cancer)')
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.show()