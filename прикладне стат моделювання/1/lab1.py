
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from matplotlib.widgets import Button, RadioButtons, TextBox

# # class DistributionSimulator:
# #     def __init__(self):        
# #         self.n_bin = 102
# #         self.p_bin = 11 / 21
        
# #         self.num_points = 1
        
# #         self.gen_k = []
# #         self.gen_gamma = []
        
# #         self.setup_math()
# #         self.setup_ui()
 
# #     def setup_math(self):
# #         self.binom_k = np.arange(0, self.n_bin + 1)
# #         p_binom = [(1 - self.p_bin)**self.n_bin]
# #         for k in range(1, self.n_bin + 1):
# #             next_p = p_binom[-1] * ((self.n_bin - k + 1) / k) * (self.p_bin / (1 - self.p_bin))
# #             p_binom.append(next_p)
# #         self.binom_pmf = np.array(p_binom)
# #         self.binom_cdf = np.cumsum(self.binom_pmf)
# #         # print(self.binom_pmf,"pmf")
# #         # print(self.binom_cdf,"cdf")

# #     def setup_ui(self):
# #         self.fig, (self.ax_dist, self.ax_line) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [60, 1]})
# #         self.ax_line.set_visible(False)
# #         plt.subplots_adjust(bottom=0.3, hspace=0.3)

# #         ax_text = plt.axes([0.45, 0.15, 0.15, 0.05])
# #         self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial='1')
# #         self.textbox.on_submit(self.update_count)

# #         ax_btn = plt.axes([0.45, 0.05, 0.2, 0.08])
# #         self.btn = Button(ax_btn, 'Згенерувати')
# #         self.btn.on_clicked(self.generate)
        
# #         self.draw_theoretical()
# #         plt.show()

# #     def update_count(self, text):
# #         try:
# #             val = int(text)
# #             self.num_points = max(1, val)
# #         except ValueError:
# #             self.textbox.set_val(str(self.num_points))

# #     def draw_theoretical(self):
# #         self.ax_dist.clear()
# #         self.ax_line.clear()

    
# #         k_arr = self.binom_k
# #         pmf = self.binom_pmf
# #         cdf = self.binom_cdf
# #         title = f'Біномний розподіл (n=102, p≈0.524)'
        
# #         self.ax_dist.set_xlim(30, 75) 
        
# #         self.ax_line.axvspan(0, 1, alpha=0.1, color='blue')
        
# #         for p in cdf[35:70]:
# #             self.ax_line.axvline(p, color='white', linewidth=0.5)

# #         self.ax_dist.bar(k_arr, pmf, color='gray', alpha=0.3, width=1.0, edgecolor='black', label='Теоретична ймовірність')
# #         self.ax_dist.set_title(title)
# #         self.ax_dist.set_ylabel('Відносна частота / Ймовірність')
# #         self.ax_dist.legend(loc='upper right')

# #         self.ax_line.set_xlim(0, 1)
# #         self.ax_line.set_ylim(0, 1)
# #         self.ax_line.get_yaxis().set_visible(False)
# #         self.ax_line.set_title("Відрізок [0, 1] (Інтервали ймовірностей)")

# #     def clear(self, event):        
# #         self.gen_k.clear()
# #         self.gen_gamma.clear()
# #         self.update_plots()
        
# #     def generate(self, event):
# #         k_arr, cdf = self.binom_k, self.binom_cdf

# #         gammas = np.random.uniform(0, 1, self.num_points)
        
# #         indices = np.searchsorted(cdf, gammas)
# #         k_results = k_arr[np.clip(indices, 0, len(k_arr) - 1)]

# #         self.gen_k.extend(k_results)
# #         self.gen_gamma.extend(gammas)
# #         print(len(self.gen_k), "точок згенеровано.")
# #         print(len(self.gen_gamma), "γ згенеровано.")
# #         self.update_plots()

# #     def update_plots(self):
# #         for patch in reversed(self.ax_dist.patches[len(self.binom_k):]):
# #             patch.remove()
# #         [line.remove() for line in self.ax_line.lines[1:]] # Видаляємо старі точки

# #         unique_k, counts = np.unique(self.gen_k, return_counts=True)
# #         frequencies = counts / len(self.gen_k)

# #         self.ax_dist.bar(unique_k, frequencies, color='red', alpha=0.5, width=0.6, label='Емпірична частота' if len(self.gen_k) == self.num_points else "")
        
# #         y_jitter = np.random.uniform(0.2, 0.8, len(self.gen_gamma[-self.num_points:]))
# #         self.ax_line.plot(self.gen_gamma[-self.num_points:], y_jitter, 'ko', markersize=3, alpha=0.5)

# #         handles, labels = self.ax_dist.get_legend_handles_labels()
# #         by_label = dict(zip(labels, handles))
# #         self.ax_dist.legend(by_label.values(), by_label.keys(), loc='upper right')
        
# #         self.fig.canvas.draw_idle()

# # if __name__ == '__main__':
# #     app = DistributionSimulator()








# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Button, TextBox

# class DistributionSimulator:
#     def __init__(self):        
#         self.n_bin = 102
#         self.p_bin = 11 / 21
        
#         self.num_points = 1
        
#         self.gen_k = []
#         self.gen_gamma = []
        
#         self.setup_math()
#         self.setup_ui()
 
#     def setup_math(self):
#         # Масив можливих значень k від 0 до n
#         self.binom_k = np.arange(0, self.n_bin + 1)
        
#         # Обчислення PMF (ймовірностей)
#         p_binom = [(1 - self.p_bin)**self.n_bin]
#         for k in range(1, self.n_bin + 1):
#             next_p = p_binom[-1] * ((self.n_bin - k + 1) / k) * (self.p_bin / (1 - self.p_bin))
#             p_binom.append(next_p)
            
#         self.binom_pmf = np.array(p_binom)
#         # Обчислення CDF (функції розподілу)
#         self.binom_cdf = np.cumsum(self.binom_pmf)

#     def setup_ui(self):
#         # Залишаємо лише один графік, оскільки відрізок нам більше не потрібен
#         self.fig, self.ax_dist = plt.subplots(figsize=(10, 6))
#         plt.subplots_adjust(bottom=0.25)

#         # UI Елементи
#         ax_text = plt.axes([0.15, 0.05, 0.15, 0.06])
#         self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial='1')
#         self.textbox.on_submit(self.update_count)

#         ax_btn = plt.axes([0.35, 0.05, 0.2, 0.06])
#         self.btn = Button(ax_btn, 'Згенерувати')
#         self.btn.on_clicked(self.generate)
        
#         ax_clear = plt.axes([0.6, 0.05, 0.2, 0.06])
#         self.btn_clear = Button(ax_clear, 'Очистити дані')
#         self.btn_clear.on_clicked(self.clear)
        
#         self.update_plots()
#         plt.show()

#     def update_count(self, text):
#         try:
#             val = int(text)
#             self.num_points = max(1, val)
#         except ValueError:
#             self.textbox.set_val(str(self.num_points))

#     def clear(self, event):        
#         self.gen_k.clear()
#         self.gen_gamma.clear()
#         self.update_plots()
        
#     def generate(self, event):
#         gammas = np.random.uniform(0, 1, self.num_points)
        
#         # Визначаємо, в які інтервали потрапили згенеровані числа
#         indices = np.searchsorted(self.binom_cdf, gammas)
#         k_results = self.binom_k[np.clip(indices, 0, len(self.binom_k) - 1)]

#         self.gen_k.extend(k_results)
#         self.gen_gamma.extend(gammas)
        
#         print(f"Згенеровано точок загалом: {len(self.gen_k)}")
#         self.update_plots()

#     def update_plots(self):
#         self.ax_dist.clear()
        
#         # Налаштування меж та підписів
#         self.ax_dist.set_xlim(35, 75)
#         self.ax_dist.set_ylim(0, 1.05)
#         self.ax_dist.set_title('Функція розподілу: Теоретична vs Емпірична')
#         self.ax_dist.set_ylabel('F(x)')
#         self.ax_dist.set_xlabel('Значення k')
#         self.ax_dist.grid(True, linestyle='--', alpha=0.5)

#         # 1. Рахуємо емпіричну функцію розподілу, якщо є згенеровані точки
#         emp_cdf = np.zeros_like(self.binom_cdf)
#         if len(self.gen_k) > 0:
#             unique_k, counts = np.unique(self.gen_k, return_counts=True)
#             total_points = len(self.gen_k)
#             current_cum = 0
            
#             for i, k in enumerate(self.binom_k):
#                 if k in unique_k:
#                     # Знаходимо кількість випадань конкретного k
#                     idx = np.where(unique_k == k)[0][0]
#                     current_cum += counts[idx]
#                 emp_cdf[i] = current_cum / total_points

#         # 2. Малюємо сходинки (відрізки зі стрілочками)
#         # Малюємо лише в діапазоні від 30 до 80 для оптимізації
#         for i in range(30, 80):
#             # Теоретична (сіра)
#             y_th = self.binom_cdf[i]
#             self.ax_dist.hlines(y_th, i, i+1, color='gray', linewidth=2)
#             self.ax_dist.plot(i+1, y_th, marker='>', color='gray', markersize=6)
            
#             # Емпірична (червона)
#             if len(self.gen_k) > 0:
#                 y_emp = emp_cdf[i]
#                 # Малюємо трохи зміщеною, щоб лінії не зливалися повністю
#                 self.ax_dist.hlines(y_emp, i, i+1, color='red', linewidth=1.5, alpha=0.8)
#                 self.ax_dist.plot(i+1, y_emp, marker='>', color='red', markersize=4, alpha=0.8)

#         # Фіктивні графіки суто для відображення легенди
#         self.ax_dist.plot([], [], color='gray', marker='>', label='Теоретична F(x)')
#         if len(self.gen_k) > 0:
#             self.ax_dist.plot([], [], color='red', marker='>', label='Емпірична F*(x)')
            
#         self.ax_dist.legend(loc='lower right')
#         self.fig.canvas.draw_idle()

# if __name__ == '__main__':
#     app = DistributionSimulator()



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox

class DistributionSimulator:
    def __init__(self):        
        self.n_bin = 102
        self.p_bin = 11 / 21
        
        self.num_points = 1
        
        self.gen_k = []
        
        self.setup_math()
        self.setup_ui()
 
    def setup_math(self):
        # Масив можливих значень k від 0 до n
        self.binom_k = np.arange(0, self.n_bin + 1)
        
        # Обчислення PMF (функція маси ймовірності - "стовпчики")
        p_binom = [(1 - self.p_bin)**self.n_bin]
        for k in range(1, self.n_bin + 1):
            next_p = p_binom[-1] * ((self.n_bin - k + 1) / k) * (self.p_bin / (1 - self.p_bin))
            p_binom.append(next_p)
            
        self.binom_pmf = np.array(p_binom)
        
        # Обчислення CDF (кумулятивна функція розподілу - "сходинки")
        self.binom_cdf = np.cumsum(self.binom_pmf)

    def setup_ui(self):
        # Створюємо 2 графіки: PMF зверху, CDF знизу
        self.fig, (self.ax_pmf, self.ax_cdf) = plt.subplots(2, 1, figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2, hspace=0.3)

        # UI Елементи
        ax_text = plt.axes([0.15, 0.05, 0.15, 0.06])
        self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial='1')
        self.textbox.on_submit(self.update_count)

        ax_btn = plt.axes([0.35, 0.05, 0.2, 0.06])
        self.btn = Button(ax_btn, 'Згенерувати')
        self.btn.on_clicked(self.generate)
        
        ax_clear = plt.axes([0.6, 0.05, 0.2, 0.06])
        self.btn_clear = Button(ax_clear, 'Очистити дані')
        self.btn_clear.on_clicked(self.clear)
        
        self.update_plots()
        plt.show()

    def update_count(self, text):
        try:
            val = int(text)
            self.num_points = max(1, val)
        except ValueError:
            self.textbox.set_val(str(self.num_points))

    def clear(self, event):        
        self.gen_k.clear()
        self.update_plots()
        
    def generate(self, event):
        gammas = np.random.uniform(0, 1, self.num_points)
        
        # Визначаємо, в які інтервали потрапили згенеровані числа
        indices = np.searchsorted(self.binom_cdf, gammas)
        k_results = self.binom_k[np.clip(indices, 0, len(self.binom_k) - 1)]

        self.gen_k.extend(k_results)
        
        print(f"Згенеровано точок загалом: {len(self.gen_k)}")
        self.update_plots()

    def update_plots(self):
        self.ax_pmf.clear()
        self.ax_cdf.clear()
        
        # --- НАЛАШТУВАННЯ ОСЕЙ ---
        x_min, x_max = 35, 75 # Відображаємо лише значущу частину графіка
        
        self.ax_pmf.set_xlim(x_min, x_max)
        self.ax_pmf.set_title('PMF: Розподіл ймовірностей (Стовпчики)')
        self.ax_pmf.set_ylabel('Ймовірність P(X=k)')
        
        self.ax_cdf.set_xlim(x_min, x_max)
        self.ax_cdf.set_ylim(0, 1.05)
        self.ax_cdf.set_title('CDF: Кумулятивна функція розподілу (Сходинки)')
        self.ax_cdf.set_ylabel('F(x) = P(X ≤ x)')
        self.ax_cdf.set_xlabel('Значення k')
        self.ax_cdf.grid(True, linestyle='--', alpha=0.4)

        # --- 1. МАЛЮЄМО ТЕОРЕТИЧНІ ГРАФІКИ (СІРІ) ---
        self.ax_pmf.bar(self.binom_k, self.binom_pmf, color='gray', alpha=0.3, width=1.0, edgecolor='black', label='Теоретична PMF')
        
        for i in range(x_min - 5, x_max + 5):
            y_th = self.binom_cdf[i]
            self.ax_cdf.hlines(y_th, i, i+1, color='gray', linewidth=2)
            self.ax_cdf.plot(i+1, y_th, marker='>', color='gray', markersize=5)
            
        self.ax_cdf.plot([], [], color='gray', marker='>', label='Теоретична CDF') # Для легенди

        # --- 2. МАЛЮЄМО ЕМПІРИЧНІ ГРАФІКИ (ЧЕРВОНІ), якщо є дані ---
        if len(self.gen_k) > 0:
            unique_k, counts = np.unique(self.gen_k, return_counts=True)
            total_points = len(self.gen_k)
            
            # Емпірична PMF (частоти)
            frequencies = counts / total_points
            self.ax_pmf.bar(unique_k, frequencies, color='red', alpha=0.5, width=0.6, label='Емпірична PMF')
            
            # Розрахунок емпіричної CDF
            emp_cdf = np.zeros_like(self.binom_cdf)
            current_cum = 0
            for i, k in enumerate(self.binom_k):
                if k in unique_k:
                    idx = np.where(unique_k == k)[0][0]
                    current_cum += counts[idx]
                emp_cdf[i] = current_cum / total_points

            # Малюємо емпіричну CDF (зміщену трохи вгору/вниз, щоб не зливалася з сірою)
            for i in range(x_min - 5, x_max + 5):
                y_emp = emp_cdf[i]
                self.ax_cdf.hlines(y_emp, i, i+1, color='red', linewidth=1.5, alpha=0.8)
                self.ax_cdf.plot(i+1, y_emp, marker='>', color='red', markersize=4, alpha=0.8)
                
            self.ax_cdf.plot([], [], color='red', marker='>', label='Емпірична CDF')

        # --- ОНОВЛЕННЯ ---
        self.ax_pmf.legend(loc='upper right')
        self.ax_cdf.legend(loc='lower right')
        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    app = DistributionSimulator()