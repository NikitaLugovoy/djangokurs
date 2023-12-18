import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('fotosave.db')

# Создание курсора
cursor = conn.cursor()

# Выполнение запросов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS photosi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        photo_data BLOB NOT NULL,
        class_name TEXT NOT NULL,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Закрытие соединения
conn.close()
