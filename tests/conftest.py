import pytest
import sqlite3

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')  # Создаем базу данных в памяти
    conn.row_factory = sqlite3.Row
    yield conn  # Возвращаем соединение для тестов
    conn.close()  # Закрываем соединение после теста