# import math
# import random
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Button
# import numpy as np
# import matplotlib as mpl    
# from scipy.stats import binom

# PUASON=0
# lam=0
# #region Пуасон
# if PUASON:
#     # === 1. Математичні розрахунки ===
#     i=9
#     lam = 3/(2*i+1)  # Дисперсія і мат. сподівання 
#     print(f"λ = {lam:.4f}")
#     # k_max = 4     # Беремо k від 0 до 3, оскільки сумарна ймовірність вже > 0.999


#     # Обчислюємо ймовірності p_k за формулою Пуассона
#     p_k = []
#     k=0
#     while sum(p_k)<=1:
#         p_k.append((math.exp(-lam) * (lam**k)) / math.factorial(k))
#         k+=1
#         if k>20:
#             break
        
#     if sum(p_k)>1:
#         p_k.pop(-1)
#         k-=1
# #endregion
# else:
#     k=51#0#6
#     p=1/2#4#5
#     p_k = [binom.pmf(x, k, p) for x in range(k)]


# print("Кількість K",k)
# print("p_k:", p_k)
# # Обчислюємо межі інтервалів на відрізку [0, 1]
# cum_p = [0.0]
# for p in p_k:
#     cum_p.append(cum_p[-1] + p)

# # === 2. Налаштування інтерфейсу (Matplotlib) ===
# fig, ax = plt.subplots(figsize=(10, 3))
# plt.subplots_adjust(bottom=0.3) # Залишаємо місце для кнопки
# ax.set_xlim(0, 1)
# # ax.set_ylim(-1, 1)
# ax.set_title(f"Моделювання Пуассонівської змінної (λ ≈ {lam:.4f})")
# ax.set_xlabel("Відрізок [0, 1]")
# # ax.get_yaxis().set_visible(False) # Вісь Y нам не потрібна

# # Відмальовуємо інтервали різними кольорами
# # colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
# cmap = mpl.colormaps['Set2']  # Використовуємо колірну карту для різних інтервалів
# np.random.seed(0)  # Фіксуємо генератор випадкових чисел для відтворюваності
# colors = np.random.rand(k+1, 3)#cmap(np.linspace(0, 1, k))

# # print("Кольори для інтервалів:", colors)
# # random.shuffle(colors)

# # for i in range(k):
# #     # Зафарбовуємо зону інтервалу
# #     ax.axvspan(cum_p[i], cum_p[i+1], color=colors[i], alpha=0.6, label=f'η = {i}')
# #     # Додаємо підпис по центру інтервалу
# #     mid_point = (cum_p[i] + cum_p[i+1]) / 2
# #     ax.text(mid_point, 0.8, f'k={i}', ha='center', va='center', fontsize=12, fontweight='bold')

# # ax.legend(loc="upper left")


# # print("Ймовірності p_k:", p_k)



# # ax.plot([i for i in range(k)], p_k, 'ro-', label='графік')
# ax.plot(np.arange(0,k),p_k, 'ro-', label='графік')


# # Списки для зберігання згенерованих точок
# points_x = []
# points_y = []
# # Об'єкт графіка точок (спочатку порожній)
# scatter_plot, = ax.plot([], [], 'ko', markersize=6, markeredgecolor='white')

# # === 3. Логіка генерації ===
# def generate_point(event):
#     for i in range(5):
#         # Генеруємо рівномірне випадкове число від 0 до 1
#         gamma = random.random()

#         # Визначаємо, в який інтервал воно потрапило
#         k_result = 0
#         for i in range(k):
#             if cum_p[i] < gamma <= cum_p[i+1]:
#                 k_result = i
#                 break
                
#         # Зберігаємо точку для відображення (Y генеруємо з невеликим розкидом, щоб точки не зливалися)
#         points_x.append(gamma)
#         jitter_y = 0#0.4 + (random.random() * 0.2) 
#         points_y.append(jitter_y)

#         # Оновлюємо графік
#         scatter_plot.set_data(points_x, points_y)
#         ax.set_title(f"Згенеровано γ = {gamma:.4f}. Потрапило в зону k = {k_result} (η = {k_result})")
#         fig.canvas.draw_idle()

# # === 4. Кнопка ===
# # Задаємо координати кнопки [зліва, знизу, ширина, висота]
# ax_btn = plt.axes([0.4, 0.05, 0.25, 0.1])
# btn = Button(ax_btn, 'Згенерувати число')
# btn.on_clicked(generate_point)

# plt.show()






import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, TextBox
from typing import List, Any


class DistributionSimulator:
    """
    Симулятор розподілів (Пуассона та Біноміального).
    Візуалізує теоретичні ймовірності та генерує емпіричні дані 
    за допомогою методу оберненого перетворення (Inverse Transform Sampling).
    """

    def __init__(self, 
                 poisson_lam: float = 3 / 17, 
                 binom_n: int = 102, 
                 binom_p: float = 11 / 21) -> None:
        
        # Параметри розподілів
        self._lam: float = poisson_lam
        self._n_bin: int = binom_n
        self._p_bin: float = binom_p
        
        # Стан симулятора
        self._current_dist: str = 'Poisson'
        self._num_points: int = 1
        
        # Зберігання згенерованих даних
        self._gen_k: List[int] = []
        self._gen_gamma: List[float] = []
        
        # Ініціалізація
        self._setup_math()
        self._setup_ui()

    def _setup_math(self) -> None:
        """
        Обчислює PMF (ймовірності) та CDF (межі інтервалів) суто математично.
        """
        # --- Розподіл Пуассона ---
        self._poisson_k: np.ndarray = np.arange(0, 10)
        p_poisson: List[float] = [np.exp(-self._lam)]
        
        for k in range(1, 10):
            p_poisson.append(p_poisson[-1] * self._lam / k)
            
        self._poisson_pmf: np.ndarray = np.array(p_poisson)
        self._poisson_cdf: np.ndarray = np.cumsum(self._poisson_pmf)

        # --- Біноміальний розподіл ---
        self._binom_k: np.ndarray = np.arange(0, self._n_bin + 1)
        p_binom: List[float] = [(1 - self._p_bin) ** self._n_bin]
        
        for k in range(1, self._n_bin + 1):
            next_p = p_binom[-1] * ((self._n_bin - k + 1) / k) * (self._p_bin / (1 - self._p_bin))
            p_binom.append(next_p)
            
        self._binom_pmf: np.ndarray = np.array(p_binom)
        self._binom_cdf: np.ndarray = np.cumsum(self._binom_pmf)

    def _setup_ui(self) -> None:
        """
        Налаштовує інтерфейс користувача (графіки та віджети Matplotlib).
        """
        self.fig, (self.ax_dist, self.ax_line) = plt.subplots(
            2, 1, 
            figsize=(10, 8), 
            gridspec_kw={'height_ratios': [3, 1]}
        )
        self.fig.canvas.manager.set_window_title("Симулятор розподілів")
        plt.subplots_adjust(bottom=0.3, hspace=0.3)

        # --- Віджети ---
        ax_radio = plt.axes([0.1, 0.05, 0.2, 0.15])
        self.radio = RadioButtons(ax_radio, ('Poisson', 'Binomial'))
        self.radio.on_clicked(self._on_change_dist)

        ax_text = plt.axes([0.45, 0.15, 0.15, 0.05])
        self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial=str(self._num_points))
        self.textbox.on_submit(self._on_update_count)

        ax_btn_gen = plt.axes([0.45, 0.05, 0.2, 0.08])
        self.btn_gen = Button(ax_btn_gen, 'Згенерувати')
        self.btn_gen.on_clicked(self._on_generate)
        
        ax_btn_clear = plt.axes([0.75, 0.05, 0.15, 0.05])
        self.btn_clear = Button(ax_btn_clear, 'Очистити')
        self.btn_clear.on_clicked(self._on_clear)

        self._draw_axes()
        plt.show()

    def _on_update_count(self, text: str) -> None:
        """Обробник зміни кількості точок для генерації."""
        try:
            val = int(text)
            self._num_points = max(1, val)  # Захист від від'ємних значень та нуля
        except ValueError:
            self.textbox.set_val(str(self._num_points))

    def _on_change_dist(self, label: str) -> None:
        """Обробник перемикання типу розподілу."""
        self._current_dist = label
        self._gen_k.clear()
        self._gen_gamma.clear()
        self._draw_axes()

    def _on_clear(self, event: Any) -> None:
        """Обробник кнопки очищення згенерованих даних."""
        self._gen_k.clear()
        self._gen_gamma.clear()
        self._draw_axes()

    def _on_generate(self, event: Any) -> None:
        """Обробник кнопки генерації нових точок."""
        if self._current_dist == 'Poisson':
            k_arr, cdf = self._poisson_k, self._poisson_cdf
        else:
            k_arr, cdf = self._binom_k, self._binom_cdf

        # 1. Генерація масиву рівномірно розподілених випадкових чисел
        gammas = np.random.uniform(0, 1, self._num_points)
        
        # 2. Бінарний пошук індексів інтервалів для всього масиву одразу
        indices = np.searchsorted(cdf, gammas)
        
        # 3. Переведення індексів у значення k
        k_results = k_arr[np.clip(indices, 0, len(k_arr) - 1)]

        self._gen_k.extend(k_results.tolist())
        self._gen_gamma.extend(gammas.tolist())
        
        print(f"Згенеровано {self._num_points} точок. Всього: {len(self._gen_k)}")
        self._draw_axes()

    def _draw_axes(self) -> None:
        """
        Повністю перемальовує графіки. Це надійніше, ніж видаляти окремі елементи.
        """
        self.ax_dist.clear()
        self.ax_line.clear()

        # --- Теоретичні дані ---
        if self._current_dist == 'Poisson':
            k_arr, pmf, cdf = self._poisson_k, self._poisson_pmf, self._poisson_cdf
            title = f'Розподіл Пуассона (λ ≈ {self._lam:.3f})'
            self.ax_dist.set_xlim(-0.5, 4.5)
            
            # Інтервали на нижньому графіку
            prev = 0
            colors = plt.cm.Set3.colors
            for i, p in enumerate(cdf[:5]): 
                self.ax_line.axvspan(prev, p, alpha=0.5, color=colors[i % len(colors)])
                mid = (prev + p) / 2
                if p - prev > 0.05:
                    self.ax_line.text(mid, 0.5, f'k={i}', ha='center', va='center', rotation=90)
                prev = p
        else:
            k_arr, pmf, cdf = self._binom_k, self._binom_pmf, self._binom_cdf
            title = f'Біноміальний розподіл (n={self._n_bin}, p≈{self._p_bin:.3f})'
            self.ax_dist.set_xlim(30, 75) 
            self.ax_line.axvspan(0, 1, alpha=0.1, color='blue')
            
            # Лінії меж
            for p in cdf[35:70]:
                self.ax_line.axvline(p, color='white', linewidth=0.5)

        # Відмальовуємо теоретичний розподіл (сірий фон)
        self.ax_dist.bar(k_arr, pmf, color='gray', alpha=0.3, width=1.0, 
                         edgecolor='black', label='Теоретична ймовірність')
        self.ax_dist.set_title(title)
        self.ax_dist.set_ylabel('Відносна частота / Ймовірність')

        # --- Емпіричні дані (якщо є) ---
        if self._gen_k:
            unique_k, counts = np.unique(self._gen_k, return_counts=True)
            frequencies = counts / len(self._gen_k)
            
            self.ax_dist.bar(unique_k, frequencies, color='red', alpha=0.5, 
                             width=0.6, label='Емпірична частота')
            
            # Відображення тільки останніх N згенерованих точок на відрізку
            last_n_gammas = self._gen_gamma[-self._num_points:]
            y_jitter = np.random.uniform(0.2, 0.8, len(last_n_gammas))
            self.ax_line.plot(last_n_gammas, y_jitter, 'ko', markersize=3, alpha=0.5)

        self.ax_dist.legend(loc='upper right')

        # --- Налаштування нижнього графіка ---
        self.ax_line.set_xlim(0, 1)
        self.ax_line.set_ylim(0, 1)
        self.ax_line.get_yaxis().set_visible(False)
        self.ax_line.set_title("Відрізок [0, 1] (Інтервали ймовірностей)")

        self.fig.canvas.draw_idle()


if __name__ == '__main__':
    # Запуск програми
    app = DistributionSimulator()