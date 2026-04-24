import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GameTheoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задача протидії коаліцій")
        self.root.geometry("1100x700")
        
        self.left_frame = ttk.Frame(self.root, padding="10", width=350)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_input_panel()
        self.setup_plot_panel()
        
    def setup_input_panel(self):
        ttk.Label(self.left_frame, text="Цільові функції:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(self.left_frame, text="I_12(x, y) =").pack(anchor=tk.W)
        self.entry_i12 = ttk.Entry(self.left_frame, width=40)
        self.entry_i12.insert(0, "0.6 * (2*x**2 + 17*x*y**2 + 3*y + 67)") # Дані Варіанта 9
        self.entry_i12.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(self.left_frame, text="I_21(x, y) =").pack(anchor=tk.W)
        self.entry_i21 = ttk.Entry(self.left_frame, width=40)
        self.entry_i21.insert(0, "0.2 * (-5*y**2 + x**2*y + 2*x + 93)") # Дані Варіанта 9
        self.entry_i21.pack(anchor=tk.W, pady=(0, 20))
        
        ttk.Label(self.left_frame, text="Межі сітки [x_min, x_max, y_min, y_max]:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        bounds_frame = ttk.Frame(self.left_frame)
        bounds_frame.pack(anchor=tk.W, pady=5)
        
        ttk.Label(bounds_frame, text="X: від").grid(row=0, column=0, padx=2)
        self.entry_xmin = ttk.Entry(bounds_frame, width=5)
        self.entry_xmin.insert(0, "0")
        self.entry_xmin.grid(row=0, column=1, padx=2)
        
        ttk.Label(bounds_frame, text="до").grid(row=0, column=2, padx=2)
        self.entry_xmax = ttk.Entry(bounds_frame, width=5)
        self.entry_xmax.insert(0, "2")
        self.entry_xmax.grid(row=0, column=3, padx=2)
        
        ttk.Label(bounds_frame, text="Y: від").grid(row=1, column=0, padx=2, pady=5)
        self.entry_ymin = ttk.Entry(bounds_frame, width=5)
        self.entry_ymin.insert(0, "1")
        self.entry_ymin.grid(row=1, column=1, padx=2)
        
        ttk.Label(bounds_frame, text="до").grid(row=1, column=2, padx=2)
        self.entry_ymax = ttk.Entry(bounds_frame, width=5)
        self.entry_ymax.insert(0, "4")
        self.entry_ymax.grid(row=1, column=3, padx=2)
        
        self.calc_btn = ttk.Button(self.left_frame, text="Розрахувати та побудувати графіки", command=self.calculate_and_plot)
        self.calc_btn.pack(anchor=tk.W, pady=20, fill=tk.X)

        ttk.Label(self.left_frame, text="Результати:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.result_text = tk.Text(self.left_frame, height=10, width=40, font=('Consolas', 9))
        self.result_text.pack(anchor=tk.W, fill=tk.X)
        
    def setup_plot_panel(self):
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text="Графік I_12")
        self.notebook.add(self.tab2, text="Графік I_21")
        
        self.fig1 = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax1 = self.fig1.add_subplot(111, projection='3d')
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab1)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.fig2 = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax2 = self.fig2.add_subplot(111, projection='3d')
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab2)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def safe_eval(self, expr, x, y):
        safe_dict = {
            "x": x, "y": y, "np": np, 
            "sin": np.sin, "cos": np.cos, "tan": np.tan, 
            "pi": np.pi, "sqrt": np.sqrt
        }
        expr = expr.replace("^", "**")
        try:
            return eval(expr, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            raise ValueError(f"Помилка у формулі: {str(e)}")

    def calculate_and_plot(self):
        eq12 = self.entry_i12.get()
        eq21 = self.entry_i21.get()
        
        xmin = float(self.entry_xmin.get())
        xmax = float(self.entry_xmax.get())
        ymin = float(self.entry_ymin.get())
        ymax = float(self.entry_ymax.get())
        
        x_vals = np.linspace(xmin, xmax, 50)
        y_vals = np.linspace(ymin, ymax, 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        Z12 = self.safe_eval(eq12, X, Y)
        Z21 = self.safe_eval(eq21, X, Y)
        
        min_y_vals_12 = np.min(Z12, axis=0) 
        max_x_idx_12 = np.argmax(min_y_vals_12)
        guaranteed_x1 = x_vals[max_x_idx_12]
        
        min_y_idx_12 = np.argmin(Z12[:, max_x_idx_12])
        guaranteed_y1 = y_vals[min_y_idx_12]
        guaranteed_z1 = Z12[min_y_idx_12, max_x_idx_12]
        
        min_x_vals_21 = np.min(Z21, axis=1) 
        max_y_idx_21 = np.argmax(min_x_vals_21)
        guaranteed_y2 = y_vals[max_y_idx_21]
        
        min_x_idx_21 = np.argmin(Z21[max_y_idx_21, :])
        guaranteed_x2 = x_vals[min_x_idx_21]
        guaranteed_z2 = Z21[max_y_idx_21, min_x_idx_21]

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "--- Гарантовані результати ---\n\n")
        self.result_text.insert(tk.END, f"Коаліція 1 (керує x):\n")
        self.result_text.insert(tk.END, f"x* = {guaranteed_x1:.3f}\n")
        self.result_text.insert(tk.END, f"y* = {guaranteed_y1:.3f}\n")
        self.result_text.insert(tk.END, f"I_12* = {guaranteed_z1:.3f}\n\n")
        
        self.result_text.insert(tk.END, f"Коаліція 2 (керує y):\n")
        self.result_text.insert(tk.END, f"x* = {guaranteed_x2:.3f}\n")
        self.result_text.insert(tk.END, f"y* = {guaranteed_y2:.3f}\n")
        self.result_text.insert(tk.END, f"I_21* = {guaranteed_z2:.3f}\n")

        self.ax1.clear()
        surf1 = self.ax1.plot_surface(X, Y, Z12, cmap='viridis', alpha=0.8)
        self.ax1.scatter(guaranteed_x1, guaranteed_y1, guaranteed_z1, color='red', s=100, label='Гарант. точка')
        self.ax1.set_title("Функція I_12(x,y)")
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        self.ax1.set_zlabel('I_12')
        self.ax1.legend()
        self.canvas1.draw()
        
        self.ax2.clear()
        surf2 = self.ax2.plot_surface(X, Y, Z21, cmap='plasma', alpha=0.8)
        self.ax2.scatter(guaranteed_x2, guaranteed_y2, guaranteed_z2, color='blue', s=100, label='Гарант. точка')
        self.ax2.set_title("Функція I_21(x,y)")
        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Y')
        self.ax2.set_zlabel('I_21')
        self.ax2.legend()
        self.canvas2.draw()
            


if __name__ == "__main__":
    root = tk.Tk()
    app = GameTheoryApp(root)
    root.mainloop()