import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Підключення моделей для відновлення значень
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Завантаження набору даних
df = sns.load_dataset("penguins")
print("Розмірність початкового набору даних:", df.shape)
print("Кількість пропусків у стовпцях:\n", df.isna().sum())

# =====================================================================
# ГРАФІК 1: Візуалізація наявності пропусків (Теплова карта)
# =====================================================================
plt.figure(figsize=(10, 6))
# Жовті смуги показуватимуть місця, де відсутні дані
sns.heatmap(df.isna(), cbar=False, cmap='viridis')
plt.title("Теплова карта пропущених значень (світлий колір - пропуски)")
plt.show()

# =====================================================================
# 1. Видалення записів з пропусками
# =====================================================================
df_dropped = df.dropna()

# =====================================================================
# 2. Відновлення пропусків у числових ознаках
# =====================================================================
num_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']

imputer_median = SimpleImputer(strategy='median')
imputer_mean = SimpleImputer(strategy='mean')

df_num_median = df.copy()
df_num_median[num_cols] = imputer_median.fit_transform(df[num_cols])

df_num_mean = df.copy()
df_num_mean[num_cols] = imputer_mean.fit_transform(df[num_cols])

# =====================================================================
# ГРАФІК 2: Порівняння розподілу (Початковий vs Середнє vs Медіана)
# Показує спотворення розподілу при заповненні середнім значенням
# =====================================================================
plt.figure(figsize=(12, 6))
sns.kdeplot(df['body_mass_g'].dropna(), label='Початкові дані (без пропусків)', fill=True, alpha=0.3, color='blue')
sns.kdeplot(df_num_mean['body_mass_g'], label='Заповнення середнім', linewidth=2, color='red')
sns.kdeplot(df_num_median['body_mass_g'], label='Заповнення медіаною', linewidth=2, linestyle='--', color='green')

plt.title("Вплив методів заповнення на розподіл ознаки (маса тіла)")
plt.xlabel("Маса тіла (г)")
plt.ylabel("Щільність")
plt.legend()
plt.show()

# =====================================================================
# ГРАФІК 3: Діаграма розмаху для оцінки зміни дисперсії та викидів
# =====================================================================
plt.figure(figsize=(10, 6))
data_to_plot = pd.DataFrame({
    'Початкові дані': df['body_mass_g'],
    'Середнє значення': df_num_mean['body_mass_g'],
    'Медіана': df_num_median['body_mass_g']
})
sns.boxplot(data=data_to_plot, palette="Set2")
plt.title("Діаграма розмаху: вплив заповнення на розкид даних")
plt.ylabel("Маса тіла (г)")
plt.show()

# =====================================================================
# 3. Відновлення пропусків у категорійних ознаках
# =====================================================================
cat_cols = ['sex']

imputer_mode = SimpleImputer(strategy='most_frequent')
imputer_const_cat = SimpleImputer(strategy='constant', fill_value='Невідомо') 

df_cat_mode = df.copy()
df_cat_mode[cat_cols] = imputer_mode.fit_transform(df[cat_cols])

df_cat_const = df.copy()
df_cat_const[cat_cols] = imputer_const_cat.fit_transform(df[cat_cols])

# =====================================================================
# ГРАФІК 4: Стовпчаста діаграма для категорійних ознак
# =====================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
sns.countplot(x='sex', data=df, ax=axes[0], palette='muted').set_title("Початкові дані")
sns.countplot(x='sex', data=df_cat_mode, ax=axes[1], palette='muted').set_title("Найчастіше значення")
sns.countplot(x='sex', data=df_cat_const, ax=axes[2], palette='muted').set_title("Константа ('Невідомо')")
plt.suptitle("Зміна балансу категорій після відновлення пропусків")
plt.show()

# =====================================================================
# 4. Відновлення пропусків алгоритмами машинного навчання
# =====================================================================
knn_imputer = KNNImputer(n_neighbors=5)
df_ml_imputed = df.copy()
df_ml_imputed[num_cols] = knn_imputer.fit_transform(df[num_cols])

# =====================================================================
# ГРАФІК 5: Порівняння найкращого статистичного методу та машинного навчання
# =====================================================================
plt.figure(figsize=(10, 5))
sns.kdeplot(df['body_mass_g'].dropna(), label='Початкові дані', fill=True, alpha=0.3, color='blue')
sns.kdeplot(df_num_median['body_mass_g'], label='Заповнення медіаною', color='green', linewidth=2)
sns.kdeplot(df_ml_imputed['body_mass_g'], label='K-найближчих сусідів (KNN)', color='orange', linestyle='--', linewidth=2)
plt.title("Порівняння статистичного методу та алгоритму машинного навчання")
plt.xlabel("Маса тіла (г)")
plt.ylabel("Щільність")
plt.legend()
plt.show()












import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer, KNNImputer

# Завантаження набору даних "Титанік"
df = sns.load_dataset("titanic")
print("Розмірність початкового набору даних:", df.shape)
print("Кількість пропусків у стовпцях:\n", df.isna().sum())

# =====================================================================
# ГРАФІК 1: Візуалізація наявності пропусків (Теплова карта)
# =====================================================================
plt.figure(figsize=(10, 6))
sns.heatmap(df.isna(), cbar=False, cmap='viridis')
plt.title("Теплова карта пропущених значень (світлий колір - пропуски)")
plt.show()

# =====================================================================
# 1. Видалення записів з пропусками
# =====================================================================
# Оскільки стовпець 'deck' має >75% пропусків, dropna() видалить майже всі дані
df_dropped = df.dropna()
print(f"Записів до видалення: {len(df)}, після видалення: {len(df_dropped)}")
# Втрата становить понад 80% даних, тому для подальшого аналізу цей метод неприйнятний.

# =====================================================================
# 2. Відновлення пропусків у числових ознаках ('age' - вік)
# =====================================================================
num_cols = ['age', 'fare']

imputer_median = SimpleImputer(strategy='median')
imputer_mean = SimpleImputer(strategy='mean')

df_num_median = df.copy()
df_num_median[num_cols] = imputer_median.fit_transform(df[num_cols])

df_num_mean = df.copy()
df_num_mean[num_cols] = imputer_mean.fit_transform(df[num_cols])

# =====================================================================
# ГРАФІК 2: Порівняння розподілу (Початковий vs Середнє vs Медіана)
# =====================================================================
plt.figure(figsize=(12, 6))
sns.kdeplot(df['age'].dropna(), label='Початкові дані (без пропусків)', fill=True, alpha=0.3, color='blue')
sns.kdeplot(df_num_mean['age'], label='Заповнення середнім', linewidth=2, color='red')
sns.kdeplot(df_num_median['age'], label='Заповнення медіаною', linewidth=2, linestyle='--', color='green')

plt.title("Вплив методів заповнення на розподіл ознаки (Вік)")
plt.xlabel("Вік (роки)")
plt.ylabel("Щільність")
plt.legend()
plt.show()

# =====================================================================
# ГРАФІК 3: Діаграма розмаху для оцінки зміни дисперсії та викидів
# =====================================================================
plt.figure(figsize=(10, 6))
data_to_plot = pd.DataFrame({
    'Початкові дані': df['age'],
    'Середнє значення': df_num_mean['age'],
    'Медіана': df_num_median['age']
})
sns.boxplot(data=data_to_plot, palette="Set2")
plt.title("Діаграма розмаху: вплив заповнення на розкид віку")
plt.ylabel("Вік")
plt.show()

# =====================================================================
# 3. Відновлення пропусків у категорійних ознаках ('deck', 'embarked')
# =====================================================================
cat_cols = ['deck', 'embarked']

# Оскільки 'deck' має багато пропусків, заповнення модою створить величезне зміщення.
# Тому для 'deck' краще використати константу 'Невідомо'.
imputer_const_cat = SimpleImputer(strategy='constant', fill_value='Невідомо') 
# 'embarked' має лише 2 пропуски, тут можна використати найчастіше значення (моду).
imputer_mode = SimpleImputer(strategy='most_frequent')

df_cat_imputed = df.copy()
# Стовпець 'deck' - константою, 'embarked' - модою
# Перетворюємо тип 'deck' на рядок (string), щоб уникнути конфлікту категорій Pandas
df_cat_imputed['deck'] = df_cat_imputed['deck'].astype(str)
df_cat_imputed['deck'] = imputer_const_cat.fit_transform(df_cat_imputed[['deck']])
df_cat_imputed['embarked'] = imputer_mode.fit_transform(df_cat_imputed[['embarked']])

# =====================================================================
# ГРАФІК 4: Стовпчаста діаграма для ознаки 'deck' (Палуба)
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.countplot(x='deck', data=df.astype(str), ax=axes[0], palette='muted', order=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'nan']).set_title("Початкові дані (nan - пропуски)")
sns.countplot(x='deck', data=df_cat_imputed, ax=axes[1], palette='muted', order=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Невідомо']).set_title("Після заповнення константою")
plt.suptitle("Зміна балансу категорій для ознаки 'Палуба'")
plt.show()

# =====================================================================
# 4. Відновлення пропусків алгоритмами машинного навчання
# =====================================================================
knn_imputer = KNNImputer(n_neighbors=5)
df_ml_imputed = df.copy()
df_ml_imputed[num_cols] = knn_imputer.fit_transform(df[num_cols])

# =====================================================================
# ГРАФІК 5: Порівняння найкращого статистичного методу та машинного навчання
# =====================================================================
plt.figure(figsize=(10, 5))
sns.kdeplot(df['age'].dropna(), label='Початкові дані', fill=True, alpha=0.3, color='blue')
sns.kdeplot(df_num_median['age'], label='Заповнення медіаною', color='green', linewidth=2)
sns.kdeplot(df_ml_imputed['age'], label='K-найближчих сусідів (KNN)', color='orange', linestyle='--', linewidth=2)
plt.title("Порівняння статистичного методу та алгоритму машинного навчання (Вік)")
plt.xlabel("Вік")
plt.ylabel("Щільність")
plt.legend()
plt.show()