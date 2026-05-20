import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

class ParetoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ітераційна процедура пошуку (Варіант 9)")
        self.root.geometry("1100x600")
        
        self.df = None
        
        self.create_widgets()
        self.update_log("Систему ініціалізовано. Очікується завантаження файлу.\nЗгідно з вар. 9: Коригування X2 та X3 при незмінних Y.")

    def create_widgets(self):
        
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        
        ttk.Button(control_frame, text="Завантажити дані з файлу (CSV)", command=self.load_file).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        
        frame_d_plus = ttk.LabelFrame(control_frame, text="Межі змінних (D+-) X2, X3")
        frame_d_plus.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.d_plus_vars = {}
        for i, var in enumerate(['x21', 'x22', 'x31', 'x32']):
            ttk.Label(frame_d_plus, text=f"{var}: [").grid(row=i, column=0)
            entry_min = ttk.Entry(frame_d_plus, width=7)
            entry_min.grid(row=i, column=1)
            ttk.Label(frame_d_plus, text=";").grid(row=i, column=2)
            entry_max = ttk.Entry(frame_d_plus, width=7)
            entry_max.grid(row=i, column=3)
            ttk.Label(frame_d_plus, text="]").grid(row=i, column=4)
            self.d_plus_vars[var] = (entry_min, entry_max)

        
        frame_btn_x = ttk.Frame(control_frame)
        frame_btn_x.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_btn_x, text="Коригування X", command=self.correct_x).pack(pady=2)
        ttk.Button(frame_btn_x, text="D+- := Do", command=self.apply_x).pack(pady=2)

        
        frame_d_o = ttk.LabelFrame(control_frame, text="Межі змінних (Do) X2, X3")
        frame_d_o.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        
        self.d_o_vars = {}
        for i, var in enumerate(['x21', 'x22', 'x31', 'x32']):
            ttk.Label(frame_d_o, text=f"{var}: [").grid(row=i, column=0)
            val_min = ttk.Label(frame_d_o, width=7, background="white", relief="sunken")
            val_min.grid(row=i, column=1)
            ttk.Label(frame_d_o, text=";").grid(row=i, column=2)
            val_max = ttk.Label(frame_d_o, width=7, background="white", relief="sunken")
            val_max.grid(row=i, column=3)
            ttk.Label(frame_d_o, text="]").grid(row=i, column=4)
            self.d_o_vars[var] = (val_min, val_max)

        
        frame_b_plus = ttk.LabelFrame(control_frame, text="Межі функцій (B+-)")
        frame_b_plus.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        self.b_plus_vars = {}
        for i, var in enumerate(['y1', 'y2', 'y3']):
            ttk.Label(frame_b_plus, text=f"{var}: [").grid(row=i, column=0)
            entry_min = ttk.Entry(frame_b_plus, width=7)
            entry_min.grid(row=i, column=1)
            ttk.Label(frame_b_plus, text=";").grid(row=i, column=2)
            entry_max = ttk.Entry(frame_b_plus, width=7)
            entry_max.grid(row=i, column=3)
            ttk.Label(frame_b_plus, text="]").grid(row=i, column=4)
            self.b_plus_vars[var] = (entry_min, entry_max)

        
        frame_btn_y = ttk.Frame(control_frame)
        frame_btn_y.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame_btn_y, text="Коригування Y", command=self.correct_y).pack(pady=2)
        ttk.Button(frame_btn_y, text="B+- := Bo", command=self.apply_y).pack(pady=2)
        ttk.Button(frame_btn_y, text="Оновити графік", command=self.plot_graph).pack(pady=2)

        
        frame_b_o = ttk.LabelFrame(control_frame, text="Межі функцій (Bo)")
        frame_b_o.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        
        self.b_o_vars = {}
        for i, var in enumerate(['y1', 'y2', 'y3']):
            ttk.Label(frame_b_o, text=f"{var}: [").grid(row=i, column=0)
            val_min = ttk.Label(frame_b_o, width=7, background="white", relief="sunken")
            val_min.grid(row=i, column=1)
            ttk.Label(frame_b_o, text=";").grid(row=i, column=2)
            val_max = ttk.Label(frame_b_o, width=7, background="white", relief="sunken")
            val_max.grid(row=i, column=3)
            ttk.Label(frame_b_o, text="]").grid(row=i, column=4)
            self.b_o_vars[var] = (val_min, val_max)

        
        self.log_text = tk.Text(control_frame, height=8, width=70)
        self.log_text.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

        
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_file(self):
        filepath = filedialog.askopenfilename(
            title="Оберіть файл вибірки Dates_6.csv",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
            
        try:
            
            col_names = ['N', 'x11', 'x12', 'x13', 'x14', 'x21', 'x22', 'x31', 'x32', 'y1', 'y2', 'y3']
            self.df = pd.read_csv(filepath, sep=r'\s*/\s*', engine='python', header=None, names=col_names)
            
            self.update_bounds_from_df()
            self.update_log(f"Файл успішно завантажено. Знайдено {len(self.df)} записів.")
            self.plot_graph()
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося прочитати файл:\n{e}")
            self.update_log("Помилка завантаження файлу.")

    def update_bounds_from_df(self):
        
        vars_to_update = ['x21', 'x22', 'x31', 'x32']
        y_vars_to_update = ['y1', 'y2', 'y3']

        for var in vars_to_update:
            vmin, vmax = self.df[var].min(), self.df[var].max()
            self.d_plus_vars[var][0].delete(0, tk.END)
            self.d_plus_vars[var][0].insert(0, str(round(vmin, 3)))
            self.d_plus_vars[var][1].delete(0, tk.END)
            self.d_plus_vars[var][1].insert(0, str(round(vmax, 3)))

        for var in y_vars_to_update:
            vmin, vmax = self.df[var].min(), self.df[var].max()
            self.b_plus_vars[var][0].delete(0, tk.END)
            self.b_plus_vars[var][0].insert(0, str(round(vmin, 3)))
            self.b_plus_vars[var][1].delete(0, tk.END)
            self.b_plus_vars[var][1].insert(0, str(round(vmax, 3)))
            
            
            self.b_o_vars[var][0].config(text=str(round(vmin * 0.9, 3)))
            self.b_o_vars[var][1].config(text=str(round(vmax * 1.1, 3)))

    def plot_graph(self):
        self.ax.clear()
        if self.df is not None:
            
            self.ax.scatter(self.df['y1'], self.df['y2'], color='blue', label='Експериментальні дані', zorder=5)

            
            try:
                y1_min = float(self.b_plus_vars['y1'][0].get())
                y1_max = float(self.b_plus_vars['y1'][1].get())
                y2_min = float(self.b_plus_vars['y2'][0].get())
                y2_max = float(self.b_plus_vars['y2'][1].get())

                
                rect = patches.Rectangle((y1_min, y2_min), y1_max - y1_min, y2_max - y2_min,
                                         linewidth=2, edgecolor='red', facecolor='red', alpha=0.1, label='Область B+- (допустима)')
                self.ax.add_patch(rect)
                
                
                self.ax.set_xlim(min(self.df['y1'].min(), y1_min) * 0.8, max(self.df['y1'].max(), y1_max) * 1.2)
                self.ax.set_ylim(min(self.df['y2'].min(), y2_min) * 0.8, max(self.df['y2'].max(), y2_max) * 1.2)
                
            except ValueError:
                self.update_log("Помилка побудови меж: перевірте правильність введених даних для B+-.")

            self.ax.set_xlabel('Показник Y1')
            self.ax.set_ylabel('Показник Y2')
            self.ax.set_title('Простір зовнішніх показників (Множина значень B)')
            self.ax.legend()
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.canvas.draw()

    def update_log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def correct_x(self):
        if self.df is None:
            self.update_log("Спочатку завантажте дані з файлу!")
            return
            
        
        delta = 0.05
        try:
            for var in ['x21', 'x22', 'x31', 'x32']:
                cur_min = float(self.d_plus_vars[var][0].get())
                cur_max = float(self.d_plus_vars[var][1].get())
                
                
                if 'x2' in var:
                    new_min, new_max = cur_min - delta, cur_max + delta
                else:
                    new_min, new_max = cur_min + delta, cur_max - delta
                    
                self.d_o_vars[var][0].config(text=str(round(new_min, 3)))
                self.d_o_vars[var][1].config(text=str(round(new_max, 3)))
                
            self.update_log("Виконано обчислення нових меж (Do) для X. Перевірте вкладеність.")
        except ValueError:
             self.update_log("Помилка: Некоректні вхідні дані для меж X.")

    def apply_x(self):
        for var in ['x21', 'x22', 'x31', 'x32']:
            self.d_plus_vars[var][0].delete(0, tk.END)
            self.d_plus_vars[var][0].insert(0, self.d_o_vars[var][0].cget("text"))
            self.d_plus_vars[var][1].delete(0, tk.END)
            self.d_plus_vars[var][1].insert(0, self.d_o_vars[var][1].cget("text"))
        self.update_log("Обмеження D+- перезаписано значеннями з Do.")

    def correct_y(self):
        self.update_log("Аналіз вкладеності B+- у Bo...\nЯкщо B+- вкладено в Bo, множину Парето знайдено.")
        
        try:
            for var in ['y1', 'y2', 'y3']:
                c_min = float(self.b_plus_vars[var][0].get())
                c_max = float(self.b_plus_vars[var][1].get())
                
                self.b_o_vars[var][0].config(text=str(round(c_min + 0.1, 3)))
                self.b_o_vars[var][1].config(text=str(round(c_max - 0.1, 3)))
        except ValueError:
            pass
        self.plot_graph()

    def apply_y(self):
        for var in ['y1', 'y2', 'y3']:
            self.b_plus_vars[var][0].delete(0, tk.END)
            self.b_plus_vars[var][0].insert(0, self.b_o_vars[var][0].cget("text"))
            self.b_plus_vars[var][1].delete(0, tk.END)
            self.b_plus_vars[var][1].insert(0, self.b_o_vars[var][1].cget("text"))
        self.update_log("Обмеження B+- перезаписано значеннями з Bo.")
        self.plot_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = ParetoApp(root)
    root.mainloop()