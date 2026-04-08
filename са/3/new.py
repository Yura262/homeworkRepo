import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

from numpy.polynomial import chebyshev as cheb
from numpy.polynomial import legendre as leg
from numpy.polynomial import hermite as herm
from numpy.polynomial import laguerre as lag

class OrthogonalModelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App")
        self.root.geometry("1450x850")
        
        self.left_panel = tk.Frame(self.root, width=450, padx=10, pady=10)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.right_panel = tk.Frame(self.root, bg="white")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_controls()
        self.setup_plot_area()
        
    def setup_controls(self):
        # 1. Вибір файлів
        file_frame = tk.LabelFrame(self.left_panel, text="1. Дані (Файли)", padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(file_frame, text="X Data:").grid(row=0, column=0, sticky="w")
        self.entry_x = tk.Entry(file_frame, width=20)
        self.entry_x.insert(0, "Xi_1.csv")
        self.entry_x.grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=lambda: self.browse_file(self.entry_x)).grid(row=0, column=2)
        
        tk.Label(file_frame, text="Y Data:").grid(row=1, column=0, sticky="w")
        self.entry_y = tk.Entry(file_frame, width=20)
        self.entry_y.insert(0, "Yi_1.csv")
        self.entry_y.grid(row=1, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=lambda: self.browse_file(self.entry_y)).grid(row=1, column=2)
        
        # 2. Налаштування моделі та поліномів
        model_frame = tk.LabelFrame(self.left_panel, text="2. Налаштування моделі", padx=10, pady=10)
        model_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(model_frame, text="Тип функції:").grid(row=0, column=0, sticky="w", pady=2)
        self.poly_type = ttk.Combobox(model_frame, values=["Linear", "Standard", "Chebyshev", "Legendre","Laguerre", "Hermite"], state="readonly")
        self.poly_type.current(2) # Default to Chebyshev
        self.poly_type.grid(row=0, column=1, pady=2, sticky="ew")
        
        tk.Label(model_frame, text="Макс. Ступінь (Power):").grid(row=1, column=0, sticky="w", pady=2)
        self.poly_degree = tk.Spinbox(model_frame, from_=1, to=10, width=5)
        self.poly_degree.delete(0, "end")
        self.poly_degree.insert(0, 2)
        self.poly_degree.grid(row=1, column=1, pady=2, sticky="w")
        
        # 3. Налаштування оптимізатора
        opt_frame = tk.LabelFrame(self.left_panel, text="3. Налаштування SGD", padx=10, pady=10)
        opt_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(opt_frame, text="Кількість епох:").grid(row=0, column=0, sticky="w")
        self.epochs_entry = tk.Entry(opt_frame, width=10)
        self.epochs_entry.insert(0, "100000") # Менше епох, бо ми нормалізуємо дані
        self.epochs_entry.grid(row=0, column=1, sticky="w")
        
        # 4. Кнопка запуску
        self.btn_run = tk.Button(self.left_panel, text="▶ Run Optimization", bg="#0052cc", fg="white", 
                                 font=("Arial", 12, "bold"), command=self.start_processing)
        self.btn_run.pack(fill=tk.X, pady=15)
        
        # 5. Логи
        tk.Label(self.left_panel, text="Журнал виконання:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(self.left_panel, height=22, width=50, bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def setup_plot_area(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 8))
        self.fig.tight_layout(pad=4.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def browse_file(self, entry_widget):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)
            
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def expand_features(self, A, poly_type, degree):
        # Нормалізація факторів до [-1, 1] для стабільності поліномів
        A_min = A.min(axis=0)
        A_max = A.max(axis=0)
        range_A = np.where(A_max - A_min == 0, 1, A_max - A_min)
        A_scaled = 2 * (A - A_min) / range_A - 1
        
        if degree == 1 or poly_type == "Linear":
            return A_scaled
            
        expanded_A = [A_scaled]
        
        for d in range(2, degree + 1):
            # Створюємо масив коефіцієнтів [0, 0, ..., 1], щоб вибрати поліном ступеня d
            coeffs = [0] * d + [1] 
            
            if poly_type == "Standard":
                feat = A_scaled ** d
            elif poly_type == "Chebyshev":
                feat = cheb.chebval(A_scaled, coeffs)
            elif poly_type == "Legendre":
                feat = leg.legval(A_scaled, coeffs)
            elif poly_type == "Hermite":
                feat = herm.hermval(A_scaled, coeffs)
            elif poly_type == "Laguerre":
                feat = lag.lagval(A_scaled, coeffs)
                
            expanded_A.append(feat)
            
        return np.hstack(expanded_A)

    def solve_sgd(self, A, Y_target, epochs, lr_init=0.01):
        num_vars = A.shape[1]
        num_samples = A.shape[0]
        C = np.zeros(num_vars)

        np.random.seed(42)
        indices = np.random.randint(0, num_samples, epochs)
        
        log_interval = max(1, epochs // 5) # Виводимо лог 5 разів
        
        for t in range(epochs):
            lr = lr_init / (1 + 1e-4 * t)
            
            p = indices[t]
            A_p = A[p]
            Y_p = Y_target[p]
            
            prediction = np.dot(A_p, C)
            error = prediction - Y_p
            
            C -= lr * error * A_p
            
            if t > 0 and t % log_interval == 0:
                current_mse = np.mean((np.dot(A, C) - Y_target)**2)
                self.log(f"   [Epoch {t}] MSE: {current_mse:,.2f}")
                
        final_mse = np.mean((np.dot(A, C) - Y_target)**2)
        self.log(f"   [Final] MSE: {final_mse:,.2f}")
        return C

    def start_processing(self):
        self.btn_run.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)
        threading.Thread(target=self.process_data, daemon=True).start()

    def process_data(self):
        file_x = self.entry_x.get()
        file_y = self.entry_y.get()
        poly_type = self.poly_type.get()
        degree = int(self.poly_degree.get())
        epochs = int(self.epochs_entry.get())
        
        try:
            self.log(f"Завантаження файлів...")
            df_X = pd.read_csv(file_x)
            df_Y = pd.read_csv(file_y)
            
            features = ['X11', 'X12', 'X21', 'X22', 'X31', 'X32', 'X33']
            A_raw = df_X[features].values
            Y_data = df_Y[['Y1', 'Y2', 'Y3', 'Y4']].values
            q0_vals = df_Y['q0'].values
            
            self.log(f"Тип моделі: {poly_type}, Ступінь: {degree}")
            self.log("Масштабування до [-1, 1] та генерація поліномів...")
            A_poly = self.expand_features(A_raw, poly_type, degree)
            
            self.log(f"Кількість факторів збільшилась з {A_raw.shape[1]} до {A_poly.shape[1]}")
            self.log("-" * 40)
            
            for ax in self.axes.flatten():
                ax.clear()
            axes_flat = self.axes.flatten()
            
            for i in range(4):
                self.log(f"▶ Старт Y{i+1}:")
                Y_i = Y_data[:, i]
                b_iq0 = (np.max(Y_i) + np.min(Y_i)) / 2.0
                Y_i_centered = Y_i - b_iq0
                
                # Початковий LR можна робити великим, оскільки фактори від -1 до 1
                C_sgd = self.solve_sgd(A_poly, Y_i_centered, epochs=epochs, lr_init=0.01)
                
                # Предикція для графіка
                Y_pred = np.dot(A_poly, C_sgd) + b_iq0
                
                ax = axes_flat[i]
                ax.plot(q0_vals, Y_i, label='Actual (Фактичні)', marker='o', color='blue')
                ax.plot(q0_vals, Y_pred, label=f'Pred ({poly_type})', marker='x', linestyle='--', color='red')
                
                ax.set_title(f'Y{i+1}: {poly_type} d={degree}', fontsize=10)
                ax.set_xlabel('q0')
                ax.legend(fontsize=8)
                ax.grid(True, alpha=0.5)

            self.canvas.draw()
            self.log("=== Готово! ===")
            
        except Exception as e:
            self.log(f"ПОМИЛКА: {str(e)}")
            messagebox.showerror("Error", str(e))
            
        finally:
            self.btn_run.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrthogonalModelApp(root)
    root.mainloop()