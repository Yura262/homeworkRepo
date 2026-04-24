import sqlite3

def init_db():
    """Ініціалізація бази даних та створення таблиці, якщо вона не існує."""
    with sqlite3.connect("dictionary.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_concept(term, description):
    """Функція додавання поняття[cite: 6]."""
    with sqlite3.connect("dictionary.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO concepts (term, description) VALUES (?, ?)", (term, description))
            conn.commit()
            print(f"Поняття '{term}' успішно додано!")
        except sqlite3.IntegrityError:
            print(f"Поняття '{term}' вже існує в базі.")

def get_description(term):
    """Функція повернення опису за введеним поняттям[cite: 6]."""
    with sqlite3.connect("dictionary.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM concepts WHERE term = ?", (term,))
        result = cursor.fetchone()
        
        if result:
            print(f"{term}: {result[0]}")
        else:
            print("Поняття не знайдено.")

if __name__ == "__main__":
    init_db()
    while True:
        print("\n1. Додати поняття\n2. Знайти опис\n3. Вийти")
        choice = input("Оберіть дію: ")
        
        if choice == '1':
            t = input("Введіть поняття: ")
            d = input("Введіть опис: ")
            add_concept(t, d)
        elif choice == '2':
            t = input("Введіть поняття для пошуку: ")
            get_description(t)
        elif choice == '3':
            break
        else:
            print("Невірна команда.")