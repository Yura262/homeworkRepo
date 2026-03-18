import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, TextBox

class ContinuousSimulator:
    def __init__(self):
        # 1. Словники з параметрами та математичними функціями для кожного розподілу

        self.dists = {
        'F(x) = (x-1)^2 / 4': {
            'x_min': 1.0,                         # Нижня межа інтервалу (з умови 1 < x <= 3)
            'x_max': 3.0,                         # Верхня межа інтервалу
            'pdf': lambda x: (x - 1) / 2,         # Похідна від F(x) = ((x-1)^2)/4
            'cdf': lambda x: ((x - 1)**2) / 4,    # Функція розподілу
            'inv_cdf': lambda g: 1 + 2 * np.sqrt(g) # Обернена функція (x = F^(-1)(gamma))
        },
        'F(x) = 2*sin(x)': {
            'x_min': 0.0,                         # Нижня межа (з умови 0 < x <= pi/6)
            'x_max': np.pi / 6,                   # Верхня межа
            'pdf': lambda x: 2 * np.cos(x),       # Похідна від F(x) = 2*sin(x)
            'cdf': lambda x: 2 * np.sin(x),       # Функція розподілу
            'inv_cdf': lambda g: np.arcsin(g / 2) # Обернена функція
        }
        }
        
        self.current_name = 'F(x) = (x-1)^2 / 4'
        self.dist = self.dists[self.current_name]
        self.num_points = 1
        
        # Списки для зберігання згенерованих даних
        self.gen_x = []
        self.gen_gamma = []
        
        self.setup_ui()

    def setup_ui(self):
        # Створюємо 2 графіки: густина (PDF) зверху, функція розподілу (CDF) знизу
        self.fig, (self.ax_pdf, self.ax_cdf) = plt.subplots(2, 1, figsize=(10, 9), gridspec_kw={'height_ratios': [2, 1.5]})
        plt.subplots_adjust(bottom=0.25, hspace=0.35)

        # Елементи керування
        ax_radio = plt.axes([0.1, 0.05, 0.25, 0.12])
        self.radio = RadioButtons(ax_radio, list(self.dists.keys()))
        self.radio.on_clicked(self.change_dist)

        ax_text = plt.axes([0.45, 0.12, 0.15, 0.05])
        self.textbox = TextBox(ax_text, 'К-сть точок (N): ', initial='1')
        self.textbox.on_submit(self.update_count)

        ax_btn = plt.axes([0.45, 0.05, 0.2, 0.06])
        self.btn = Button(ax_btn, 'Згенерувати')
        self.btn.on_clicked(self.generate)

        self.draw_theoretical()
        plt.show()

    def update_count(self, text):
        try:
            val = int(text)
            self.num_points = max(1, val) # Захист від від'ємних чи нульових значень
        except ValueError:
            self.textbox.set_val(str(self.num_points)) # Відкат при введенні літер

    def change_dist(self, label):
        self.current_name = label
        self.dist = self.dists[label]
        # Очищуємо пам'ять точок при зміні розподілу
        self.gen_x.clear()
        self.gen_gamma.clear()
        self.draw_theoretical()
        self.fig.canvas.draw_idle()

    def draw_theoretical(self):
        """Відмальовує статичні "сірі" графіки теорії."""
        self.ax_pdf.clear()
        self.ax_cdf.clear()

        # Масив X для побудови ідеальних ліній
        x_vals = np.linspace(self.dist['x_min'], self.dist['x_max'], 500)
        
        # --- Верхній графік (PDF) ---
        pdf_vals = self.dist['pdf'](x_vals)
        self.ax_pdf.plot(x_vals, pdf_vals, color='black', linewidth=1.5, label='Теоретична густина f(x)')
        self.ax_pdf.fill_between(x_vals, pdf_vals, color='gray', alpha=0.2)
        
        self.ax_pdf.set_title(f"Густина розподілу (PDF) для {self.current_name}")
        self.ax_pdf.set_xlim(self.dist['x_min'], self.dist['x_max'])
        self.ax_pdf.set_ylim(0, max(pdf_vals) * 1.2)
        self.ax_pdf.set_ylabel('Щільність імовірності')
        self.ax_pdf.legend(loc='upper left')

        # --- Нижній графік (CDF) ---
        cdf_vals = self.dist['cdf'](x_vals)
        self.ax_cdf.plot(x_vals, cdf_vals, color='blue', linewidth=2, label='Функція розподілу F(x)')
        
        self.ax_cdf.set_title("Метод обернених функцій (γ → x)")
        self.ax_cdf.set_xlim(self.dist['x_min'], self.dist['x_max'])
        self.ax_cdf.set_ylim(0, 1)
        self.ax_cdf.set_xlabel('Згенероване значення (x)')
        self.ax_cdf.set_ylabel('Випадкове число (γ)')
        self.ax_cdf.legend(loc='upper left')

    def generate(self, event):
        # 1. Генеруємо базові числа γ ~ U(0,1)
        gammas = np.random.uniform(0, 1, self.num_points)
        
        # 2. Обчислюємо x через обернену функцію
        xs = self.dist['inv_cdf'](gammas)
        
        # Зберігаємо
        self.gen_gamma.extend(gammas)
        self.gen_x.extend(xs)
        
        self.update_plots(new_gammas=gammas, new_xs=xs)

    def update_plots(self, new_gammas, new_xs):
        # Відновлюємо чисту теорію (видаляємо старі гістограми та лінії)
        self.draw_theoretical()
        
        # --- Оновлення PDF (Гістограма) ---
        # Використовуємо density=True, щоб площа гістограми дорівнювала 1 (як у PDF)
        self.ax_pdf.hist(self.gen_x, bins=30, density=True, color='red', alpha=0.5, 
                         edgecolor='darkred', label=f'Емпірика (Всього: {len(self.gen_x)})')
        self.ax_pdf.legend(loc='upper left')

        # --- Оновлення CDF (Точки та лінії проекції) ---
        # Малюємо точки на самій кривій F(x)
        self.ax_cdf.scatter(self.gen_x, self.gen_gamma, color='black', s=15, zorder=5)
        
        # Якщо ми генеруємо малу кількість точок (напр. <= 10 за клік),
        # малюємо наочні пунктирні лінії від осі Y(γ) до кривої і вниз до осі X
        if self.num_points <= 10:
            for g, x in zip(new_gammas, new_xs):
                # Горизонтальна лінія від γ до кривої
                self.ax_cdf.plot([self.dist['x_min'], x], [g, g], color='red', linestyle='--', alpha=0.6)
                # Вертикальна лінія від кривої до x
                self.ax_cdf.plot([x, x], [0, g], color='red', linestyle='--', alpha=0.6)

        self.fig.canvas.draw_idle()

# Запуск додатку
if __name__ == '__main__':
    app = ContinuousSimulator()