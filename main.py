import sqlite3


def init_db():
    """Создание таблиц и наполнение тестовыми данными"""
    conn = sqlite3.connect('tech_support.db')
    cursor = conn.cursor()

    # Создаем таблицу сотрудников
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')

    # Создаем таблицу заявок в техподдержку
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL, -- 'Новая', 'В работе', 'Закрыта'
            priority TEXT NOT NULL, -- 'Низкий', 'Средний', 'Высокий'
            created_at TEXT NOT NULL, -- Дата создания
            closed_at TEXT -- Дата закрытия
        )
    ''')

    # Заполняем тестовыми данными (если таблица пустая)
    cursor.execute("SELECT COUNT(*) FROM Users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO Users (username, password, full_name) VALUES ('karipov_t', 'password123', 'Карипов Тимур')")

        tickets = [
            ('Не работает принтер в бухгалтерии', 'В работе', 'Высокий', '2026-11-10 09:00:00', None),
            ('Забыли пароль от почты', 'Новая', 'Средний', '2026-11-10 10:15:00', None),
            ('Синий экран смерти на ПК №4', 'Закрыта', 'Высокий', '2026-11-09 11:00:00', '2026-11-09 13:30:00'),
            ('Медленно работает 1С', 'В работе', 'Низкий', '2026-11-10 11:00:00', None)
        ]
        cursor.executemany(
            "INSERT INTO Tickets (title, status, priority, created_at, closed_at) VALUES (?, ?, ?, ?, ?)", tickets)

    conn.commit()
    conn.close()


def login():
    """Функция авторизации пользователя"""
    print("=== АВТОРИЗАЦИЯ В СИСТЕМЕ ТЕХПОДДЕРЖКИ ===")
    username = input("Введите логин: ")
    password = input("Введите пароль: ")

    conn = sqlite3.connect('tech_support.db')
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM Users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"\nПриветствуем, {user[0]}!")
        return True
    else:
        print("\nОшибка: Неверный логин или пароль!")
        return False


def show_active_tickets():
    """Вывод списка активных (не закрытых) заявок"""
    conn = sqlite3.connect('tech_support.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status, priority FROM Tickets WHERE status != 'Закрыта'")
    tickets = cursor.fetchall()
    conn.close()

    print("\n=== СПИСОК АКТИВНЫХ ЗАЯВОК ===")
    print(f"{'ID':<4} | {'Название заявки':<40} | {'Статус':<10} | {'Приоритет'}")
    print("-" * 75)
    for t in tickets:
        print(f"{t[0]:<4} | {t[1]:<40} | {t[2]:<10} | {t[3]}")


if __name__ == '__main__':
    init_db()  # Инициализируем БД
    if login():
        show_active_tickets()
