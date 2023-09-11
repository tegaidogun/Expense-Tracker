import os
import sqlite3

def init_db():
    if os.path.exists('expenses.db'):
        os.remove('expenses.db')

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY, 
            username TEXT UNIQUE, 
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY, 
            amount REAL, 
            description TEXT, 
            date TEXT,
            month TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
