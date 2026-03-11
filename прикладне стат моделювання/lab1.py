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

class DistributionSimulator:
    def __init__(self):
        # Параметри Пуассона
        self.lam = 3 / 17
        
        # Параметри Біноміального
        self.n_bin = 102
        self.p_bin = 11 / 21
        
        self.current_dist = 'Poisson'
        self.num_points = 1
        
        # Зберігання згенерованих даних
        self.gen_k = []
        self.gen_gamma = []
        
        self.setup_math()
        self.setup_ui()
 
    def setup_math(self):
        """Обчислює PMF (ймовірності) та CDF (межі інтервалів) суто математично, без готових чорних скриньок"""
        # Пуассон (рахуємо до k=10, цього достатньо для λ=0.176)
        self.poisson_k = np.arange(0, 10)
        p_poisson = [np.exp(-self.lam)]
        for k in range(1, 10):
            p_poisson.append(p_poisson[-1] * self.lam / k)
        self.poisson_pmf = np.array(p_poisson)
        self.poisson_cdf = np.cumsum(self.poisson_pmf)

        # Біноміальний (рахуємо для всіх k від 0 до n)
        self.binom_k = np.arange(0, self.n_bin + 1)
        p_binom = [(1 - self.p_bin)**self.n_bin]
        for k in range(1, self.n_bin + 1):
            next_p = p_binom[-1] * ((self.n_bin - k + 1) / k) * (self.p_bin / (1 - self.p_bin))
            p_binom.append(next_p)
        self.binom_pmf = np.array(p_binom)
        self.binom_cdf = np.cumsum(self.binom_pmf)

    def setup_ui(self):
        # Створюємо 2 графіки: зверху розподіл (3/4 висоти), знизу відрізок (1/4 висоти)
        self.fig, (self.ax_dist, self.ax_line) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        plt.subplots_adjust(bottom=0.3, hspace=0.3)

        # Додаємо віджети
        ax_radio = plt.axes([0.1, 0.05, 0.2, 0.15])
        self.radio = RadioButtons(ax_radio, ('Poisson', 'Binomial'))
        self.radio.on_clicked(self.change_dist)

        ax_text = plt.axes([0.45, 0.15, 0.15, 0.05])
        self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial='1')
        self.textbox.on_submit(self.update_count)

        ax_btn = plt.axes([0.45, 0.05, 0.2, 0.08])
        self.btn = Button(ax_btn, 'Згенерувати')
        self.btn.on_clicked(self.generate)
        
        axC_btn = plt.axes([0.75, 0.05, 0.1, 0.04])
        self.btnC = Button(axC_btn, 'Очистити')
        self.btnC.on_clicked(self.clear)

        self.draw_theoretical()
        plt.show()

    def update_count(self, text):
        try:
            val = int(text)
            self.num_points = max(1, val) # Не менше 1
        except ValueError:
            self.textbox.set_val(str(self.num_points)) # Повертаємо попереднє дійсне значення

    def change_dist(self, label):
        self.current_dist = label
        self.gen_k.clear()
        self.gen_gamma.clear()
        self.draw_theoretical()
        self.fig.canvas.draw_idle()

    def draw_theoretical(self):
        self.ax_dist.clear()
        self.ax_line.clear()

        if self.current_dist == 'Poisson':
            k_arr = self.poisson_k
            pmf = self.poisson_pmf
            cdf = self.poisson_cdf
            title = f'Розподіл Пуассона (λ ≈ 0.176)'
            self.ax_dist.set_xlim(-0.5, 4.5) # Обрізаємо порожній хвіст
            
            # Малюємо інтервали на нижньому графіку
            prev = 0
            colors = plt.cm.Set3.colors
            for i, p in enumerate(cdf[:5]): # Візуалізуємо тільки перші 5 зон, бо далі вони мікроскопічні
                self.ax_line.axvspan(prev, p, alpha=0.5, color=colors[i % len(colors)])
                mid = (prev + p) / 2
                if p - prev > 0.05: # Підписуємо тільки достатньо широкі інтервали
                    self.ax_line.text(mid, 0.5, f'k={i}', ha='center', va='center', rotation=90)
                prev = p
        else:
            k_arr = self.binom_k
            pmf = self.binom_pmf
            cdf = self.binom_cdf
            title = f'Біноміальний розподіл (n=102, p≈0.524)'
            
            # 1. Центруємо графік навколо мат. сподівання (~53.4)
            self.ax_dist.set_xlim(30, 75) 
            
            self.ax_line.axvspan(0, 1, alpha=0.1, color='blue')
            
            # 2. Малюємо лінії меж для тих k, де є реальні зміни ймовірності (наприклад, від 35 до 70)
            for p in cdf[35:70]:
                self.ax_line.axvline(p, color='white', linewidth=0.5)

        # Відмальовуємо сірий бекграунд (теоретичний розподіл)
        self.ax_dist.bar(k_arr, pmf, color='gray', alpha=0.3, width=1.0, edgecolor='black', label='Теоретична ймовірність')
        self.ax_dist.set_title(title)
        self.ax_dist.set_ylabel('Відносна частота / Ймовірність')
        self.ax_dist.legend(loc='upper right')

        # Налаштування нижнього графіка
        self.ax_line.set_xlim(0, 1)
        self.ax_line.set_ylim(0, 1)
        self.ax_line.get_yaxis().set_visible(False)
        self.ax_line.set_title("Відрізок [0, 1] (Інтервали ймовірностей)")

    def clear(self, event):        
        self.gen_k.clear()
        self.gen_gamma.clear()
        self.update_plots()
        
    def generate(self, event):
        if self.current_dist == 'Poisson':
            k_arr, cdf = self.poisson_k, self.poisson_cdf
        else:
            k_arr, cdf = self.binom_k, self.binom_cdf

        # 1. Відчитуємо масив випадкових чисел γ
        gammas = np.random.uniform(0, 1, self.num_points)
        
        # 2. Шукаємо індекси інтервалів для всього масиву одразу (бінарний пошук)
        indices = np.searchsorted(cdf, gammas)
        
        # 3. Переводимо індекси у значення k
        k_results = k_arr[np.clip(indices, 0, len(k_arr) - 1)]

        self.gen_k.extend(k_results)
        self.gen_gamma.extend(gammas)
        print(len(self.gen_k), "точок згенеровано.")
        print(len(self.gen_gamma), "γ згенеровано.")
        # self.draw_theoretical()
        self.update_plots()
        # self.fig.canvas.draw_idle()

    def update_plots(self):
        # Видаляємо старі емпіричні дані (щоб не нашаровувати)
        for patch in reversed(self.ax_dist.patches[len(self.binom_k if self.current_dist == 'Binomial' else self.poisson_k):]):
            patch.remove()
        [line.remove() for line in self.ax_line.lines[1:]] # Видаляємо старі точки

        # Рахуємо унікальні згенеровані k та їх частоту
        unique_k, counts = np.unique(self.gen_k, return_counts=True)
        frequencies = counts / len(self.gen_k)

        # Накладаємо емпіричний розподіл
        self.ax_dist.bar(unique_k, frequencies, color='red', alpha=0.5, width=0.6, label='Емпірична частота' if len(self.gen_k) == self.num_points else "")
        
        # Додаємо точки на відрізок (з Y-розкидом, щоб вони не злипались в одну лінію)
        y_jitter = np.random.uniform(0.2, 0.8, len(self.gen_gamma[-self.num_points:]))
        self.ax_line.plot(self.gen_gamma[-self.num_points:], y_jitter, 'ko', markersize=3, alpha=0.5)

        # Оновлюємо легенду та відмальовуємо
        handles, labels = self.ax_dist.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax_dist.legend(by_label.values(), by_label.keys(), loc='upper right')
        
        self.fig.canvas.draw_idle()

# Запуск програми
if __name__ == '__main__':
    app = DistributionSimulator()