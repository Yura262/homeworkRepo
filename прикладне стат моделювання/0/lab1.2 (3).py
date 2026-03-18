# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Button, RadioButtons, TextBox

# class ContinuousSimulator:
#     def __init__(self):
#         self.dists = {
#         'F(x) = (x-1)^2 / 4': {
#             'x_min': 1.0,                         # Нижня межа інтервалу 
#             'x_max': 3.0,                         # Верхня межа інтервалу
#             'pdf': lambda x: (x - 1) / 2,         # Похідна від F(x)
#             'cdf': lambda x: ((x - 1)**2) / 4,    # Функція розподілу
#             'inv_cdf': lambda g: 1 + 2 * np.sqrt(g) # Обернена функція 
#         }
#         }
        
#         self.current_name = 'F(x) = (x-1)^2 / 4'
#         self.dist = self.dists[self.current_name]
#         self.num_points = 1
        
#         self.gen_x = []
#         self.gen_gamma = []
        
#         self.setup_ui()

#     def setup_ui(self):
#         self.fig, (self.ax_pdf, self.ax_cdf) = plt.subplots(2, 1, figsize=(10, 9), gridspec_kw={'height_ratios': [200, 1.5]})
#         self.ax_cdf.set_visible(False)
#         plt.subplots_adjust(bottom=0.25, hspace=0.35)
#         # ax_radio = plt.axes([0.1, 0.05, 0.25, 0.12])
#         # self.radio = RadioButtons(ax_radio, list(self.dists.keys()))
#         # self.radio.on_clicked(self.change_dist)
        
#         ax_text = plt.axes([0.45, 0.12, 0.15, 0.05])
#         self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial='1')
#         self.textbox.on_submit(self.update_count)

#         ax_btn = plt.axes([0.45, 0.05, 0.2, 0.06])
#         self.btn = Button(ax_btn, 'Згенерувати')
#         self.btn.on_clicked(self.generate)

#         self.draw_theoretical()
#         plt.show()

#     def update_count(self, text):
#         try:
#             val = int(text)
#             self.num_points = max(1, val) 
#         except ValueError:
#             self.textbox.set_val(str(self.num_points)) 

#     def change_dist(self, label):
#         self.current_name = label
#         self.dist = self.dists[label]
#         self.gen_x.clear()
#         self.gen_gamma.clear()
#         self.draw_theoretical()
#         self.fig.canvas.draw_idle()

#     def draw_theoretical(self):
#         self.ax_pdf.clear()
#         self.ax_cdf.clear()

#         x_vals = np.linspace(self.dist['x_min'], self.dist['x_max'], 500)
        
#         pdf_vals = self.dist['pdf'](x_vals)
#         self.ax_pdf.plot(x_vals, pdf_vals, color='black', linewidth=1.5, label='Теоретична густина f(x)')
#         self.ax_pdf.fill_between(x_vals, pdf_vals, color='gray', alpha=0.2)
        
#         self.ax_pdf.set_title(f"Густина розподілу для {self.current_name}")
#         self.ax_pdf.set_xlim(self.dist['x_min'], self.dist['x_max'])
#         self.ax_pdf.set_ylim(0, max(pdf_vals) * 1.2)
#         self.ax_pdf.set_ylabel('Щільність імовірності')
#         self.ax_pdf.legend(loc='upper left')

#         cdf_vals = self.dist['cdf'](x_vals)
#         self.ax_cdf.plot(x_vals, cdf_vals, color='blue', linewidth=2, label='Функція розподілу F(x)')
        
#         self.ax_cdf.set_title("Метод обернених функцій (γ → x)")
#         self.ax_cdf.set_xlim(self.dist['x_min'], self.dist['x_max'])
#         self.ax_cdf.set_ylim(0, 1)
#         self.ax_cdf.set_xlabel('Згенероване значення (x)')
#         self.ax_cdf.set_ylabel('Випадкове число (γ)')
#         self.ax_cdf.legend(loc='upper left')

#     def generate(self, event):
#         gammas = np.random.uniform(0, 1, self.num_points)
        
#         xs = self.dist['inv_cdf'](gammas)
        
#         self.gen_gamma.extend(gammas)
#         self.gen_x.extend(xs)
        
#         self.update_plots(new_gammas=gammas, new_xs=xs)

#     def update_plots(self, new_gammas, new_xs):
#         self.draw_theoretical()
        
#         self.ax_pdf.hist(self.gen_x, bins=30, density=True, color='red', alpha=0.5, 
#                          edgecolor='darkred', label=f'Емпірична густина (Всього: {len(self.gen_x)})')
#         self.ax_pdf.legend(loc='upper left')

#         self.ax_cdf.scatter(self.gen_x, self.gen_gamma, color='black', s=15, zorder=5)
        
#         if self.num_points <= 10:
#             for g, x in zip(new_gammas, new_xs):
#                 self.ax_cdf.plot([self.dist['x_min'], x], [g, g], color='red', linestyle='--', alpha=0.6)
#                 self.ax_cdf.plot([x, x], [0, g], color='red', linestyle='--', alpha=0.6)

#         self.fig.canvas.draw_idle()

# if __name__ == '__main__':
#     app = ContinuousSimulator()







import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox

class ContinuousSimulator:
    def __init__(self):
        self.dists = {
            'F(x) = (x-1)^2 / 4': {
                'x_min': 1.0,
                'x_max': 3.0,
                # np.where дозволяє задати "нулі по краях" за межами [1, 3]
                'pdf': lambda x: np.where((x >= 1) & (x <= 3), (x - 1) / 2, 0),
                'cdf': lambda x: np.where(x < 1, 0, np.where(x > 3, 1, ((x - 1)**2) / 4)),
                'inv_cdf': lambda g: 1 + 2 * np.sqrt(g)
            }
        }
        
        self.current_name = 'F(x) = (x-1)^2 / 4'
        self.dist = self.dists[self.current_name]
        self.num_points = 1
        
        self.gen_x = []
        self.gen_gamma = []
        
        self.setup_ui()

    def setup_ui(self):
        # Робимо два рівноцінних графіки: PDF (зверху) та CDF (знизу)
        self.fig, (self.ax_pdf, self.ax_cdf) = plt.subplots(2, 1, figsize=(10, 9))
        plt.subplots_adjust(bottom=0.25, hspace=0.35)
        
        # Поле для вводу кількості точок
        ax_text = plt.axes([0.15, 0.12, 0.15, 0.05])
        self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial='1')
        self.textbox.on_submit(self.update_count)

        # Кнопка генерації
        ax_btn = plt.axes([0.35, 0.11, 0.2, 0.07])
        self.btn = Button(ax_btn, 'Згенерувати')
        self.btn.on_clicked(self.generate)

        # Кнопка очищення
        ax_clear = plt.axes([0.6, 0.11, 0.2, 0.07])
        self.btn_clear = Button(ax_clear, 'Очистити дані')
        self.btn_clear.on_clicked(self.clear)

        self.draw_theoretical()
        plt.show()

    def update_count(self, text):
        try:
            val = int(text)
            self.num_points = max(1, val) 
        except ValueError:
            self.textbox.set_val(str(self.num_points)) 

    def clear(self, event):        
        self.gen_x.clear()
        self.gen_gamma.clear()
        self.draw_theoretical()
        self.fig.canvas.draw_idle()

    def draw_theoretical(self):
        self.ax_pdf.clear()
        self.ax_cdf.clear()

        # Беремо ширший проміжок (від 0 до 4), щоб побачити "нулі по краях"
        plot_min, plot_max = 0.0, 4.0
        x_vals = np.linspace(plot_min, plot_max, 500)
        
        # --- 1. Графік щільності (PDF) ---
        pdf_vals = self.dist['pdf'](x_vals)
        self.ax_pdf.plot(x_vals, pdf_vals, color='black', linewidth=1.5, label='Теоретична щільність f(x)')
        
        # Зафарбовуємо лише корисну площу (від x_min до x_max)
        x_fill = np.linspace(self.dist['x_min'], self.dist['x_max'], 100)
        self.ax_pdf.fill_between(x_fill, self.dist['pdf'](x_fill), color='gray', alpha=0.2)
        
        self.ax_pdf.set_title(f"PDF: Щільність розподілу (з нулями по краях)")
        self.ax_pdf.set_xlim(plot_min, plot_max)
        self.ax_pdf.set_ylim(-0.1, max(pdf_vals) * 1.3)
        self.ax_pdf.set_ylabel('f(x)')
        self.ax_pdf.grid(True, linestyle='--', alpha=0.5)
        self.ax_pdf.legend(loc='upper left')

        # --- 2. Графік функції розподілу (CDF) ---
        cdf_vals = self.dist['cdf'](x_vals)
        self.ax_cdf.plot(x_vals, cdf_vals, color='blue', linewidth=2, label='Теоретична CDF F(x)')
        
        self.ax_cdf.set_title("CDF: Метод обернених функцій (γ → x)")
        self.ax_cdf.set_xlim(plot_min, plot_max)
        self.ax_cdf.set_ylim(-0.05, 1.05)
        self.ax_cdf.set_xlabel('Значення (x)')
        self.ax_cdf.set_ylabel('Ймовірність / Випадкове число (γ)')
        self.ax_cdf.grid(True, linestyle='--', alpha=0.5)
        self.ax_cdf.legend(loc='upper left')

    def generate(self, event):
        gammas = np.random.uniform(0, 1, self.num_points)
        xs = self.dist['inv_cdf'](gammas)
        
        self.gen_gamma.extend(gammas)
        self.gen_x.extend(xs)
        
        self.update_plots(new_gammas=gammas, new_xs=xs)

    def update_plots(self, new_gammas, new_xs):
        self.draw_theoretical()
        
        # Емпірична гістограма (PDF)
        if len(self.gen_x) > 0:
            self.ax_pdf.hist(self.gen_x, bins=30, density=True, color='red', alpha=0.5, 
                             edgecolor='darkred', label=f'Емпірична щільність (N={len(self.gen_x)})')
            self.ax_pdf.legend(loc='upper left')

            # Емпірична функція розподілу (CDF)
            sorted_x = np.sort(self.gen_x)
            ecdf_y = np.arange(1, len(sorted_x) + 1) / len(sorted_x)
            self.ax_cdf.step(sorted_x, ecdf_y, color='red', alpha=0.7, linewidth=1.5, label='Емпірична CDF', where='post')
            self.ax_cdf.legend(loc='upper left')

        # Відображення "шляху" генерації для останніх точок (пунктирні лінії)
        if self.num_points <= 10:
            for g, x in zip(new_gammas, new_xs):
                # Лінія від осі Y (γ) до кривої F(x)
                self.ax_cdf.plot([0, x], [g, g], color='red', linestyle='--', alpha=0.6)
                # Лінія від кривої F(x) вниз до осі X (отримане x)
                self.ax_cdf.plot([x, x], [0, g], color='red', linestyle='--', alpha=0.6)
                # Точка на самій кривій
                self.ax_cdf.scatter([x], [g], color='black', s=20, zorder=5)

        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    app = ContinuousSimulator()