import sqlite3
import os

from lib.utils import db_location

def get_connection():
    return sqlite3.connect(f'{db_location}/backup_db.db')

def get_cursor():
    return get_connection().cursor()

def create_table():
    print("Creating table")
    get_cursor().execute("CREATE TABLE IF NOT EXISTS backup (filename text)")
    get_connection().commit()


def insert_data(table, filename):
    conn = get_connection()
    conn.cursor().execute(f"INSERT INTO {table} VALUES (?)", (f"{filename}",))
    conn.commit()
    
def get_data():
    return [row for row in get_cursor().execute("SELECT * FROM backup")]