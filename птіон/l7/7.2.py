import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- Оголошення класів згідно із завданням ---

class Person:
    def __init__(self):
        self.name = None
        self.byear = None

    def input_data(self, name, byear):
        """Адаптований метод введення для GUI."""
        self.name = name
        self.byear = self.check_by(byear)

    @staticmethod
    def check_by(by, cur_year=datetime.now().year):
        """Виправлений метод перевірки року народження з PDF[cite: 22, 23, 24]."""
        by = int(by)
        # Працівнику має бути від 17 до 65 років 
        if by in range(cur_year - 65, cur_year - 17):
            return by
        else:
            raise ValueError("Некоректний вік працівника (має бути 17-65 років)")


class Employee(Person):
    def __init__(self):
        super().__init__()
        self.emp_id = None      # Табельний номер [cite: 33]
        self.hourly_rate = 0.0
        self.timesheet = {}     # day: hours

    def calculate_salary(self, min_daily_hours=8):
        """Розрахунок зарплати за відпрацьованими годинами[cite: 33, 38]."""
        total_salary = 0.0
        for day, hours in self.timesheet.items():
            total_salary += hours * self.hourly_rate
        return total_salary


# --- Робота з Базою Даних ---

def init_db():
    """Створення структури бази даних для працівників та табелів[cite: 40, 41]."""
    with sqlite3.connect("company.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                byear INTEGER NOT NULL,
                hourly_rate REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timesheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id INTEGER,
                day INTEGER NOT NULL,
                hours REAL NOT NULL,
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
            )
        ''')
        conn.commit()


# --- Графічний інтерфейс (GUI) ---

class CompanyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обчислення заробітної плати")
        self.root.geometry("600x400")

        init_db()

        # Фрейм списку працівників 
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Прізвище", "Зарплата за місяць"), show="headings")
        self.tree.heading("ID", text="Таб. №")
        self.tree.heading("Прізвище", text="Прізвище")
        self.tree.heading("Зарплата за місяць", text="Зарплата (грн)")
        self.tree.pack(fill="both", expand=True)

        # Панель кнопок
        self.btn_frame = ttk.Frame(self.root)
        self.btn_frame.pack(fill="x", padx=10, pady=10)

        self.btn_add = ttk.Button(self.btn_frame, text="Додати працівника", command=self.add_employee_window)
        self.btn_add.pack(side="left", padx=5)

        self.btn_timesheet = ttk.Button(self.btn_frame, text="Заповнити табель", command=self.open_timesheet_window)
        self.btn_timesheet.pack(side="left", padx=5)

        self.btn_refresh = ttk.Button(self.btn_frame, text="Оновити список", command=self.load_data)
        self.btn_refresh.pack(side="right", padx=5)

        self.load_data()

    def load_data(self):
        """Завантаження працівників та розрахунок їхньої зарплати на льоту."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        with sqlite3.connect("company.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT emp_id, name, byear, hourly_rate FROM employees")
            employees_data = cursor.fetchall()

            for emp_data in employees_data:
                emp = Employee()
                emp.emp_id = emp_data[0]
                emp.name = emp_data[1]
                emp.byear = emp_data[2]
                emp.hourly_rate = emp_data[3]

                # Отримання табелю
                cursor.execute("SELECT day, hours FROM timesheets WHERE emp_id=?", (emp.emp_id,))
                timesheets_data = cursor.fetchall()
                for t_data in timesheets_data:
                    emp.timesheet[t_data[0]] = t_data[1]

                # Розрахунок
                salary = emp.calculate_salary()
                self.tree.insert("", "end", values=(emp.emp_id, emp.name, f"{salary:.2f}"))

    def add_employee_window(self):
        top = tk.Toplevel(self.root)
        top.title("Новий працівник")

        ttk.Label(top, text="Табельний номер:").grid(row=0, column=0, padx=5, pady=5)
        entry_id = ttk.Entry(top)
        entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top, text="Прізвище:").grid(row=1, column=0, padx=5, pady=5)
        entry_name = ttk.Entry(top)
        entry_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(top, text="Рік народження:").grid(row=2, column=0, padx=5, pady=5)
        entry_byear = ttk.Entry(top)
        entry_byear.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(top, text="Погодинна ставка (грн):").grid(row=3, column=0, padx=5, pady=5)
        entry_rate = ttk.Entry(top)
        entry_rate.grid(row=3, column=1, padx=5, pady=5)

        def save_employee():
            try:
                emp = Employee()
                emp.input_data(entry_name.get(), entry_byear.get()) # Викличе перевірку року
                
                with sqlite3.connect("company.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO employees (emp_id, name, byear, hourly_rate) VALUES (?, ?, ?, ?)",
                        (int(entry_id.get()), emp.name, emp.byear, float(entry_rate.get()))
                    )
                    conn.commit()
                messagebox.showinfo("Успіх", "Працівника додано!")
                self.load_data()
                top.destroy()
            except Exception as e:
                messagebox.showerror("Помилка", str(e))

        ttk.Button(top, text="Зберегти", command=save_employee).grid(row=4, columnspan=2, pady=10)

    def open_timesheet_window(self):
        """Окреме вікно для введення табелю[cite: 40, 41]."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Оберіть працівника зі списку!")
            return

        item = self.tree.item(selected[0])
        emp_id = item['values'][0]
        emp_name = item['values'][1]

        top = tk.Toplevel(self.root)
        top.title(f"Табель: {emp_name} (Таб. №{emp_id})")

        ttk.Label(top, text="День місяця (1-31):").grid(row=0, column=0, padx=5, pady=5)
        entry_day = ttk.Entry(top)
        entry_day.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top, text="Відпрацьовано годин:").grid(row=1, column=0, padx=5, pady=5)
        entry_hours = ttk.Entry(top)
        entry_hours.grid(row=1, column=1, padx=5, pady=5)

        def save_timesheet():
            try:
                day = int(entry_day.get())
                hours = float(entry_hours.get())
                if not (1 <= day <= 31):
                    raise ValueError("День має бути від 1 до 31")

                with sqlite3.connect("company.db") as conn:
                    cursor = conn.cursor()
                    # Перевіряємо, чи є вже запис за цей день, і оновлюємо або вставляємо
                    cursor.execute("SELECT id FROM timesheets WHERE emp_id=? AND day=?", (emp_id, day))
                    existing = cursor.fetchone()
                    if existing:
                        cursor.execute("UPDATE timesheets SET hours=? WHERE id=?", (hours, existing[0]))
                    else:
                        cursor.execute("INSERT INTO timesheets (emp_id, day, hours) VALUES (?, ?, ?)", (emp_id, day, hours))
                    conn.commit()
                messagebox.showinfo("Успіх", "Табель оновлено!")
                self.load_data()
                entry_day.delete(0, tk.END)
                entry_hours.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Помилка", str(e))

        ttk.Button(top, text="Додати/Оновити години", command=save_timesheet).grid(row=2, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyApp(root)
    root.mainloop()