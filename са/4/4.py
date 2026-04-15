import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy.polynomial import chebyshev

import pandas as pd
import numpy as np

def load_custom_data(file_path):
    df = pd.read_csv(file_path, sep='/', header=None)
  
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    X1 = df[[1, 2]].values.astype(float)
    X2 = df[[3, 4]].values.astype(float)
    X3 = df[[5, 6, 7]].values.astype(float)
    
    Y = df[[8, 9, 10, 11]].values.astype(float)
    
    return X1, X2, X3, Y



class SystemAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Відновлення функціональних залежностей в мультиплікативній формі")
        self.root.geometry("900x600")
        
        self.create_widgets()
        
        self.q0 = 45
        self.x = np.linspace(0, 50, self.q0)
        self.y_real = 100 + np.sin(self.x / 5) * 50 + np.cos(self.x / 2) * 20
        self.y_real[28:32] -= 80 
        
    def create_widgets(self):
        frame_params = tk.LabelFrame(self.root, text="Параметри", padx=10, pady=10)
        frame_params.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        
        tk.Label(frame_params, text="Розмір вибірки").grid(row=0, column=0, sticky="w")
        self.entry_samples = tk.Entry(frame_params, width=10)
        self.entry_samples.insert(0, "45")
        self.entry_samples.grid(row=0, column=1, sticky="w")
        
        tk.Label(frame_params, text="Точність").grid(row=1, column=0, sticky="w")
        self.entry_precision = tk.Entry(frame_params, width=10)
        self.entry_precision.insert(0, "1e-7")
        self.entry_precision.grid(row=1, column=1, sticky="w")
        
        tk.Label(frame_params, text="Степені поліномів:").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        poly_frame = tk.Frame(frame_params)
        poly_frame.grid(row=3, column=0, columnspan=2, sticky="w")
        tk.Label(poly_frame, text="P1").pack(side=tk.LEFT)
        self.p1 = tk.Entry(poly_frame, width=5); self.p1.insert(0, "3"); self.p1.pack(side=tk.LEFT, padx=5)
        tk.Label(poly_frame, text="P2").pack(side=tk.LEFT)
        self.p2 = tk.Entry(poly_frame, width=5); self.p2.insert(0, "3"); self.p2.pack(side=tk.LEFT, padx=5)
        tk.Label(poly_frame, text="P3").pack(side=tk.LEFT)
        self.p3 = tk.Entry(poly_frame, width=5); self.p3.insert(0, "3"); self.p3.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_params, text="Вигляд поліномів").grid(row=4, column=0, sticky="w", pady=(10,0))
        self.poly_type = ttk.Combobox(frame_params, values=["Чебишова", "Лежандра", "Лагерра"], width=12)
        self.poly_type.current(0)
        self.poly_type.grid(row=4, column=1, sticky="w", pady=(10,0))
        
        self.half_sample_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_params, text="Половина вибірки", variable=self.half_sample_var).grid(row=5, column=0, columnspan=2, sticky="w", pady=5)
        
        frame_dims = tk.LabelFrame(self.root, text="Розмірності", padx=10, pady=10)
        frame_dims.grid(row=1, column=0, padx=10, pady=5, sticky="nwe")
        tk.Label(frame_dims, text="x1: 2\nx2: 2\nx3: 3\nY: 4", justify=tk.LEFT).pack(anchor="w")

        frame_middle = tk.Frame(self.root)
        frame_middle.grid(row=0, column=1, padx=10, pady=5, sticky="nw")
        
        frame_weights = tk.LabelFrame(frame_middle, text="Ваги цільових функцій", padx=10, pady=10)
        frame_weights.pack(fill="x", pady=5)
        self.weight_var = tk.IntVar(value=1)
        tk.Radiobutton(frame_weights, text="Середнє арифметичне", variable=self.weight_var, value=1).pack(anchor="w")
        tk.Radiobutton(frame_weights, text="Через максимум і мінімум", variable=self.weight_var, value=2).pack(anchor="w")
        
        frame_files = tk.Frame(frame_middle)
        frame_files.pack(fill="x", pady=10)
        tk.Label(frame_files, text="Файл вихідних даних").grid(row=0, column=0, sticky="w")
        self.file_in = tk.Entry(frame_files, width=15); self.file_in.insert(0, "in.txt")
        self.file_in.grid(row=0, column=1, padx=5)
        tk.Button(frame_files, text="...", command=lambda: self.file_in.insert(0, filedialog.askopenfilename())).grid(row=0, column=2)
        
        tk.Label(frame_files, text="Файл результатів").grid(row=1, column=0, sticky="w", pady=5)
        self.file_out = tk.Entry(frame_files, width=15); self.file_out.insert(0, "out.html")
        self.file_out.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame_files, text="...").grid(row=1, column=2, pady=5)
        
        self.lbl_delta_minus = tk.Label(frame_middle, text="Delta minus = ")
        self.lbl_delta_minus.pack(anchor="w", pady=2)
        self.lbl_delta_plus = tk.Label(frame_middle, text="Delta plus = ")
        self.lbl_delta_plus.pack(anchor="w", pady=2)

        frame_right = tk.Frame(self.root)
        frame_right.grid(row=0, column=2, padx=10, pady=5, sticky="nw")
        
        frame_method = tk.LabelFrame(frame_right, text="Метод пошуку Lambda", padx=10, pady=10)
        frame_method.pack(fill="x", pady=5)
        self.method_var = tk.IntVar(value=2)
        tk.Radiobutton(frame_method, text="З однієї системи рівнянь", variable=self.method_var, value=1).pack(anchor="w")
        tk.Radiobutton(frame_method, text="З трьох систем рівнянь", variable=self.method_var, value=2).pack(anchor="w")
        
        tk.Button(frame_right, text="Пуск", width=15, command=self.run_calculation).pack(pady=10)
        tk.Button(frame_right, text="Перегляд", width=15).pack(pady=5)

        self.frame_plot = tk.Frame(self.root)
        self.frame_plot.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        frame_slider = tk.Frame(self.root)
        frame_slider.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        tk.Label(frame_slider, text="Цільова функція:").pack(side=tk.LEFT)
        self.slider = ttk.Scale(frame_slider, from_=1, to=4, orient=tk.HORIZONTAL, length=400)
        self.slider.set(4)
        self.slider.pack(side=tk.LEFT, padx=10)
        
        self.ax.set_facecolor('#f0f0f0')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.canvas.draw()

    def run_calculation(self):
        try:
            X1, X2, X3, Y = load_custom_data('task4_Dates.csv')
            
            target_idx = int(self.slider.get()) - 1
            y_real = Y[:, target_idx]
            x_axis = np.arange(len(y_real))

            p_deg = int(self.p1.get())
            coeffs = np.polynomial.chebyshev.chebfit(x_axis, y_real, deg=p_deg)
            y_pred = np.polynomial.chebyshev.chebval(x_axis, coeffs)

            self.ax.clear()
            self.ax.plot(x_axis, y_real, 'k-', label=f"Вихідна Y{target_idx+1}")
            self.ax.plot(x_axis, y_pred, 'r--', label="Відновлена модель")
            self.ax.legend()
            self.canvas.draw()
            
            delta = np.max(np.abs(y_real - y_pred))
            self.lbl_delta_plus.config(text=f"Max Error = {delta:.4e}")

        except Exception as e:
            print(f"Помилка завантаження: {e}")
            
            
            
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SystemAnalysisApp(root)
    root.mainloop()