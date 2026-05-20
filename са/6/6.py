import tkinter as tk
from tkinter import messagebox

def create_gui():
    root = tk.Tk()
    root.title("Ітераційна процедура пошуку")
    root.geometry("680x480")
    root.resizable(False, False)

    

    def get_bounds(entries_dict):
        """Зчитує значення з полів і повертає словник {ключ: (min_val, max_val)}."""
        bounds = {}
        try:
            for key, (entry_min, entry_max) in entries_dict.items():
                min_val = float(entry_min.get().replace(',', '.'))
                max_val = float(entry_max.get().replace(',', '.'))
                bounds[key] = (min_val, max_val)
            return bounds
        except ValueError:
            messagebox.showerror("Помилка вводу", "Перевірте правильність введених числових даних.")
            return None

    def set_bounds(entries_dict, values_dict):
        """Записує значення у відповідні поля."""
        for key, (min_val, max_val) in values_dict.items():
            entry_min, entry_max = entries_dict[key]
            entry_min.delete(0, tk.END)
            entry_min.insert(0, str(min_val))
            entry_max.delete(0, tk.END)
            entry_max.insert(0, str(max_val))

    def log_message(message):
        """Виводить повідомлення у текстове поле."""
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, message)

    def check_inclusion(target_bounds, calc_bounds):
        """Перевіряє, чи вкладена цільова множина (target) у розраховану (calc)."""
        for key in target_bounds:
            t_min, t_max = target_bounds[key]
            c_min, c_max = calc_bounds[key]
            
            if t_min < c_min or t_max > c_max:
                return False
        return True

    

    def on_corr_x1():
        d_pm = get_bounds(entries_d_pm)
        d_o = get_bounds(entries_d_o)
        if not d_pm or not d_o: return

        if check_inclusion(d_pm, d_o):
            log_message("Процедура коригування обмежень на X1\n\nD+- вкладено в Do.\nМожна переходити до перевірки Y.")
        else:
            log_message("Процедура коригування обмежень на X1\n\nЯкщо D+- не вкладено в Do,\nпотрібно підкоригувати межі (D+-) для X1.")

    def on_assign_x():
        d_o = get_bounds(entries_d_o)
        if d_o:
            set_bounds(entries_d_pm, d_o)
            log_message("Значення Do успішно скопійовані у D+-.")

    def on_corr_y():
        b_pm = get_bounds(entries_b_pm)
        b_o = get_bounds(entries_b_o)
        if not b_pm or not b_o: return

        if check_inclusion(b_pm, b_o):
            log_message("Процедура коригування обмежень на Y\n\nB+- вкладено в Bo,\nотже B+- = B*, і область Парето знайдено.")
        else:
            log_message("Процедура коригування обмежень на Y\n\nB+- не вкладено в Bo,\nпотрібно підкоригувати межі (B+-) для функцій y1, y2, y3,\nабо перейти до процедури коригування меж для X1.")

    def on_assign_y():
        b_o = get_bounds(entries_b_o)
        if b_o:
            set_bounds(entries_b_pm, b_o)
            log_message("Значення Bo успішно скопійовані у B+-.")

    

    def create_var_block(parent, title, labels, default_values=None):
        frame = tk.LabelFrame(parent, text=title, font=("Arial", 10))
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame, text=f"{label}: [", font=("Arial", 10)).grid(row=i, column=0, padx=(5, 0), pady=5)
            
            entry_min = tk.Entry(frame, width=8)
            entry_min.grid(row=i, column=1, pady=5)
            
            tk.Label(frame, text=";", font=("Arial", 10)).grid(row=i, column=2, pady=5)
            
            entry_max = tk.Entry(frame, width=8)
            entry_max.grid(row=i, column=3, pady=5)
            
            tk.Label(frame, text="]", font=("Arial", 10)).grid(row=i, column=4, padx=(0, 5), pady=5)
            
            if default_values and label in default_values:
                entry_min.insert(0, default_values[label][0])
                entry_max.insert(0, default_values[label][1])
                
            entries[label] = (entry_min, entry_max)
        return frame, entries

    
    d_pm_defaults = {"x11": ("0", "2"), "x12": ("0", "2.2"), "x13": ("0", "2.3"), "x14": ("0", "0.16")}
    d_o_defaults = {"x11": ("0.588", "0.691"), "x12": ("0.704", "0.773"), "x13": ("0.879", "0.917"), "x14": ("0.038", "0.108")}
    
    
    frame_d_pm, entries_d_pm = create_var_block(root, "Межі змінних (D+-)", ["x11", "x12", "x13", "x14"], d_pm_defaults)
    frame_d_pm.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    frame_btn_x = tk.Frame(root)
    frame_btn_x.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(frame_btn_x, text="Коригування X1", width=15, command=on_corr_x1).pack(pady=10)
    tk.Button(frame_btn_x, text="D+- := Do", width=15, command=on_assign_x).pack(pady=10)

    frame_d_o, entries_d_o = create_var_block(root, "Межі змінних (Do)", ["x11", "x12", "x13", "x14"], d_o_defaults)
    frame_d_o.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    
    b_pm_defaults = {"y1": ("1", "7"), "y2": ("1", "5"), "y3": ("0", "4")}
    b_o_defaults = {"y1": ("1.105", "5.855"), "y2": ("0.935", "4.027"), "y3": ("0.802", "2.952")}

    
    frame_b_pm, entries_b_pm = create_var_block(root, "Межі функцій (B+-)", ["y1", "y2", "y3"], b_pm_defaults)
    frame_b_pm.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    frame_btn_y = tk.Frame(root)
    frame_btn_y.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(frame_btn_y, text="Коригування Y", width=15, command=on_corr_y).pack(pady=10)
    tk.Button(frame_btn_y, text="B+- := Bo", width=15, command=on_assign_y).pack(pady=10)

    frame_b_o, entries_b_o = create_var_block(root, "Межі функцій (Bo)", ["y1", "y2", "y3"], b_o_defaults)
    frame_b_o.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

    
    frame_log = tk.Frame(root)
    frame_log.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="we")
    
    global log_text
    log_text = tk.Text(frame_log, height=6, width=80, font=("Arial", 10), wrap="word")
    log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(frame_log, command=log_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_text.config(yscrollcommand=scrollbar.set)
    
    log_text.insert(tk.END, "Програма готова до роботи. Змініть межі та натисніть кнопки коригування для перевірки.")

    root.mainloop()

if __name__ == "__main__":
    create_gui()