import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ParetoOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Завдання1")
        self.root.geometry("1150x850")

        # frames
        input_frame = ttk.LabelFrame(root, text="Вхідні дані", padding=10)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        plot_frame = ttk.Frame(root)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Inputs
        # f1 
        ttk.Label(input_frame, text="f1(x):").grid(row=0, column=0, sticky="e")
        self.entry_f1 = ttk.Entry(input_frame, width=25)
        self.entry_f1.insert(0, "2 - 3*x + x^3")
        self.entry_f1.grid(row=0, column=1, padx=5, pady=2)

        self.opt1 = ttk.Combobox(input_frame, values=["min", "max"], width=5, state="readonly")
        self.opt1.set("min")
        self.opt1.grid(row=0, column=2, padx=2)

        ttk.Label(input_frame, text="Обмеження:").grid(row=0, column=3, sticky="e")
        self.sign1 = ttk.Combobox(input_frame, values=["<=", ">="], width=4, state="readonly")
        self.sign1.set("<=")
        self.sign1.grid(row=0, column=4, padx=2)
        
        self.entry_f1_lim = ttk.Entry(input_frame, width=10)
        self.entry_f1_lim.insert(0, "1")
        self.entry_f1_lim.grid(row=0, column=5, padx=5, pady=2)

        # f2 
        ttk.Label(input_frame, text="f2(x):").grid(row=1, column=0, sticky="e")
        self.entry_f2 = ttk.Entry(input_frame, width=25)
        self.entry_f2.insert(0, "16 - x^2")
        self.entry_f2.grid(row=1, column=1, padx=5, pady=2)

        self.opt2 = ttk.Combobox(input_frame, values=["min", "max"], width=5, state="readonly")
        self.opt2.set("max")
        self.opt2.grid(row=1, column=2, padx=2)

        ttk.Label(input_frame, text="Обмеження:").grid(row=1, column=3, sticky="e")
        self.sign2 = ttk.Combobox(input_frame, values=["<=", ">="], width=4, state="readonly")
        self.sign2.set(">=")
        self.sign2.grid(row=1, column=4, padx=2)

        self.entry_f2_lim = ttk.Entry(input_frame, width=10)
        self.entry_f2_lim.insert(0, "3")
        self.entry_f2_lim.grid(row=1, column=5, padx=5, pady=2)

        # range X
        ttk.Label(input_frame, text="Межі X (min, max):").grid(row=2, column=0, sticky="e")
        range_frame = ttk.Frame(input_frame)
        range_frame.grid(row=2, column=1, columnspan=2, sticky="w")
        
        self.entry_xmin = ttk.Entry(range_frame, width=10)
        self.entry_xmin.insert(0, "-1")
        self.entry_xmin.pack(side=tk.LEFT, padx=5)
        
        self.entry_xmax = ttk.Entry(range_frame, width=10)
        self.entry_xmax.insert(0, "4")
        self.entry_xmax.pack(side=tk.LEFT, padx=5)

        # calculate button
        self.btn_calc = ttk.Button(input_frame, text="Розрахувати та Побудувати", command=self.calculate)
        self.btn_calc.grid(row=2, column=3, columnspan=3, sticky="ew", padx=5, pady=5)

        # text area
        self.result_text = tk.Text(input_frame, height=6, width=100)
        self.result_text.grid(row=3, column=0, columnspan=6, pady=10)

        # init
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def parse_function(self, func_str, x_val):
        try:
            func_str = func_str.replace("^", "**")
            allowed_names = {
                "x": x_val,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "exp": np.exp, "sqrt": np.sqrt, "log": np.log, "lg": np.log10,
                "abs": np.abs, "pi": np.pi
            }
            return eval(func_str, {"__builtins__": {}}, allowed_names)
        except Exception as e:
            raise ValueError(f"Помилка у формулі: {e}")

    def calculate(self):
        try:
            # Зчитування параметрів
            f1_str = self.entry_f1.get()
            f2_str = self.entry_f2.get()
            f1_lim = float(self.entry_f1_lim.get())
            f2_lim = float(self.entry_f2_lim.get())
            x_min = float(self.entry_xmin.get())
            x_max = float(self.entry_xmax.get())

            # Генерація сітки
            step = 0.001
            x = np.arange(x_min, x_max + step, step)
            x = np.round(x, 3)

            # Обчислення функцій
            y1 = self.parse_function(f1_str, x)
            y2 = self.parse_function(f2_str, x)

            # Фільтрація допустимої множини
            m1 = (y1 <= f1_lim) if self.sign1.get() == "<=" else (y1 >= f1_lim)
            m2 = (y2 <= f2_lim) if self.sign2.get() == "<=" else (y2 >= f2_lim)
            mask = m1 & m2
            
            valid_x = x[mask]
            valid_y1 = y1[mask]
            valid_y2 = y2[mask]

            if len(valid_x) == 0:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Результат: Допустима множина порожня. Жодна точка не задовольняє обмеженням.")
                self.ax1.clear()
                self.ax2.clear()
                self.canvas.draw()
                return

            # Визначення точок Парето
            pareto_mask = np.ones(len(valid_x), dtype=bool)
            opt1_sign = 1 if self.opt1.get() == "max" else -1
            opt2_sign = 1 if self.opt2.get() == "max" else -1

            # Пошук домінуючих точок
            for i in range(len(valid_x)):
                b_eq1 = (valid_y1 * opt1_sign) >= (valid_y1[i] * opt1_sign)
                b_eq2 = (valid_y2 * opt2_sign) >= (valid_y2[i] * opt2_sign)
                str_b1 = (valid_y1 * opt1_sign) > (valid_y1[i] * opt1_sign)
                str_b2 = (valid_y2 * opt2_sign) > (valid_y2[i] * opt2_sign)
                
                dominators = (b_eq1 & b_eq2) & (str_b1 | str_b2)
                if np.any(dominators):
                    pareto_mask[i] = False

            pareto_x = valid_x[pareto_mask]
            pareto_y1 = valid_y1[pareto_mask]
            pareto_y2 = valid_y2[pareto_mask]

            # Звуження множини Парето (тех обмеження)
            if f1_lim == 0 or f2_lim == 0:
                raise ValueError("Порогові обмеження не можуть дорівнювати нулю")

            norm_y1 = pareto_y1 / f1_lim
            norm_y2 = pareto_y2 / f2_lim

            # Максимін: max(min(f1/f1*, f2/f2*))
            min_vals = np.minimum(norm_y1, norm_y2)
            idx_maximin = np.argmax(min_vals)
            x_maximin = pareto_x[idx_maximin]

            # Мінімакс: min(max(f1/f1*, f2/f2*))
            max_vals = np.maximum(norm_y1, norm_y2)
            idx_minimax = np.argmin(max_vals)
            x_minimax = pareto_x[idx_minimax]

            # виведення результатів
            intervals = []
            if len(pareto_x) > 0:
                start_x, prev_x = pareto_x[0], pareto_x[0]
                for px in pareto_x[1:]:
                    if px > prev_x + step * 1.5:
                        intervals.append(f"[{start_x:.3f}; {prev_x:.3f}]")
                        start_x = px
                    prev_x = px
                intervals.append(f"[{start_x:.3f}; {prev_x:.3f}]")

            res_str = f"Множина Парето лежить в інтервалах x: {', '.join(intervals)}\n"
            res_str += "-"*60 + "\n"
            res_str += f"Раціональний компроміс (Максимін): x = {x_maximin:.3f} | f1 = {pareto_y1[idx_maximin]:.3f}, f2 = {pareto_y2[idx_maximin]:.3f}\n"
            res_str += f"Раціональний компроміс (Мінімакс): x = {x_minimax:.3f} | f1 = {pareto_y1[idx_minimax]:.3f}, f2 = {pareto_y2[idx_minimax]:.3f}"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, res_str)

            self.ax1.clear()
            self.ax2.clear()

            # графік 1 Простір змінних
            self.ax1.plot(x, y1, label='f1(x)', color='blue', alpha=0.5)
            self.ax1.plot(x, y2, label='f2(x)', color='green', alpha=0.5)
            self.ax1.axhline(f1_lim, color='blue', linestyle='--', alpha=0.5)
            self.ax1.axhline(f2_lim, color='green', linestyle='--', alpha=0.5)
            
            self.ax1.scatter(pareto_x, pareto_y1, color='red', s=5, zorder=5, label='Pareto f1')
            self.ax1.scatter(pareto_x, pareto_y2, color='orange', s=5, zorder=5, label='Pareto f2')
            
            self.ax1.axvline(x_maximin, color='purple', linestyle=':', label='Максимін')
            self.ax1.axvline(x_minimax, color='cyan', linestyle=':', label='Мінімакс')

            self.ax1.set_title("Простір змінних (X)")
            self.ax1.set_xlabel("x")
            self.ax1.set_ylabel("Значення функцій")
            self.ax1.legend(loc='best')
            self.ax1.grid(True)

            # графік 2 Простір критеріїв
            self.ax2.scatter(valid_y1, valid_y2, c='gray', alpha=0.3, label='Допустима множина')
            self.ax2.scatter(pareto_y1, pareto_y2, c='red', s=15, label='Множина Парето')

            self.ax2.scatter(pareto_y1[idx_maximin], pareto_y2[idx_maximin], c='purple', marker='*', s=150, label='Максимін', zorder=10)
            self.ax2.scatter(pareto_y1[idx_minimax], pareto_y2[idx_minimax], c='cyan', marker='P', s=100, label='Мінімакс', zorder=10)

            self.ax2.set_title("Простір критеріїв (f1 vs f2)")
            self.ax2.set_xlabel(f"f1 ({self.opt1.get()})")
            self.ax2.set_ylabel(f"f2 ({self.opt2.get()})")
            self.ax2.legend(loc='best')
            self.ax2.grid(True)

            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Помилка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ParetoOptimizerApp(root)
    root.mainloop()