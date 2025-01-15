import sqlite3


# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('my_database.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблицы
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpu TEXT NOT NULL,
        ram_av TEXT NOT NULL,
        ram_tot TEXT NOT NULL,
        disk_av TEXT NOT NULL,
        disk_tot TEXT NOT NULL
    )
    ''')
    conn.commit()

# Вставка данных
def insert_data(conn, cpu, ram_av, ram_tot, disk_av, disk_tot):
    """
    Вставляет данные в таблицу notes.
    """
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO notes (cpu, ram_av, ram_tot, disk_av, disk_tot)
    VALUES (?, ?, ?, ?, ?)
    ''', (cpu, ram_av, ram_tot, disk_av, disk_tot))
    conn.commit()

def return_data(conn):
    """
    Возвращает все данные из таблицы notes.
    Если таблица не существует, возвращает пустой список.
    """
    cursor = conn.cursor()
    
    # Проверяем, существует ли таблица notes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Если таблица не существует, возвращаем пустой список
        return []
    
    # Если таблица существует, выполняем запрос и возвращаем данные
    cursor.execute('SELECT * FROM notes')
    rows = cursor.fetchall()
    return [list(row) for row in rows]
