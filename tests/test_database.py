import pytest
import sqlite3
from database import get_db_connection, create_tables, insert_data, return_data
from conftest import db_connection

def test_get_db_connection(db_connection):
    conn = get_db_connection()
    assert conn is not None
    assert isinstance(conn, sqlite3.Connection)

def test_create_tables(db_connection):
    create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
    result = cursor.fetchone()
    assert result is not None  

def test_insert_data(db_connection):
    create_tables(db_connection)
    insert_data(db_connection, "15.5", "5.8", "16.0", "120.5", "500.0")
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    assert len(rows) == 1  
    assert rows[0][1] == "15.5" 
    assert rows[0][2] == "5.8"
    assert rows[0][3] == "16.0"
    assert rows[0][4] == "120.5"
    assert rows[0][5] == "500.0"

def test_return_data(db_connection):
    # Проверяем, что возвращается пустой список, если таблица пуста
    empty_data = return_data(db_connection)
    assert len(empty_data) == 0

    # Добавляем данные
    create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
    INSERT INTO notes (cpu, ram_av, ram_tot, disk_av, disk_tot)
    VALUES (?, ?, ?, ?, ?)
    ''', ("15.5", "5.8", "16.0", "120.5", "500.0"))
    cursor.execute('''
    INSERT INTO notes (cpu, ram_av, ram_tot, disk_av, disk_tot)
    VALUES (?, ?, ?, ?, ?)
    ''', ("20.0", "8.0", "32.0", "240.0", "1000.0"))
    db_connection.commit()

    # Проверяем, что возвращаются все данные
    rows = return_data(db_connection)
    assert len(rows) == 2 
    assert rows[0][1] == "15.5" 
    assert rows[1][1] == "20.0" 

def test_insert_and_return_data(db_connection):
    create_tables(db_connection)
    insert_data(db_connection, "15.5", "5.8", "16.0", "120.5", "500.0")
    # Получаем данные
    rows = return_data(db_connection)
    # Проверяем, что данные корректны
    assert len(rows) == 1
    assert rows[0][1] == "15.5"