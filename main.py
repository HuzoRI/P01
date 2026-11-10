import sqlite3
from datetime import datetime


def init_db():
    """Создание таблиц и наполнение тестовыми данными"""
    conn = sqlite3.connect('tech_support.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            created_at TEXT NOT NULL,
            closed_at TEXT
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM Users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO Users (username, password, full_name) VALUES ('karipov_t', 'password123', 'Карипов Тимур')")

        # Добавим больше закрытых заявок с разными датами для точности эксперимента
        tickets = [
            ('Не работает принтер в бухгалтерии', 'В работе', 'Высокий', '2026-11-10 09:00:00', None),
            ('Забыли пароль от почты', 'Новая', 'Средний', '2026-11-10 10:15:00', None),
            ('Синий экран смерти на ПК №4', 'Закрыта', 'Высокий', '2026-11-09 11:00:00', '2026-11-09 13:30:00'),
            # Решено за 2.5 часа
            ('Не запускается браузер', 'Закрыта', 'Низкий', '2026-11-08 10:00:00', '2026-11-08 11:15:00'),
            # Решено за 1.25 часа
            ('Сбой корпоративной сети', 'Закрыта', 'Высокий', '2026-11-07 14:00:00', '2026-11-07 18:00:00'),
            # Решено за 4 часа
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


def run_computational_experiment():
    """
    ВЫЧИСЛИТЕЛЬНЫЙ ЭКСПЕРИМЕНТ:
    Расчет среднего времени выполнения заявок (в часах) на основе дат из БД.
    Оценка эффективности обработки инцидентов для регламента SLA.
    """
    print("\n=== ЗАПУСК ВЫЧИСЛИТЕЛЬНОГО ЭКСПЕРИМЕНТА ===")
    conn = sqlite3.connect('tech_support.db')
    cursor = conn.cursor()

    # Берем только закрытые заявки, у которых есть дата создания и закрытия
    cursor.execute("SELECT created_at, closed_at FROM Tickets WHERE status = 'Закрыта'")
    closed_tickets = cursor.fetchall()
    conn.close()

    if not closed_tickets:
        print("Недостаточно данных для проведения эксперимента.")
        return

    total_hours = 0
    count = len(closed_tickets)

    for created, closed in closed_tickets:
        # Превращаем строки из БД в объекты дат
        time_start = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
        time_end = datetime.strptime(closed, "%Y-%m-%d %H:%M:%S")

        # Считаем разницу во времени в часах
        duration = time_end - time_start
        hours = duration.total_seconds() / 3600
        total_hours += hours

    # Главное математическое вычисление эксперимента
    average_resolution_time = total_hours / count

    print(f"Успешно обработано закрытых заявок для анализа: {count} шт.")
    print(f"⏱️ Математическое среднее время решения одной заявки: {average_resolution_time:.2f} час(ов).")

    # Элемент анализа/эксперимента
    if average_resolution_time <= 3.0:
        print("Результат: Скорость ответов соответствует норме SLA (≤ 3 часов).")
    else:
        print("Результат: Рекомендуется нанять дополнительных инженеров, норма SLA превышена!")


if __name__ == '__main__':
    init_db()
    if login():
        show_active_tickets()
        # Вызываем новый функционал Версии 2
        run_computational_experiment()
