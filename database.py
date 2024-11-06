import sqlite3


# Database connection function
def connect_db():
    conn = sqlite3.connect('books.db')
    return conn


# Create the table for the first time
def create_table():
    with connect_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                publication_date DATE NOT NULL,
                isbn TEXT NOT NULL,
                category TEXT NOT NULL
            );
        ''')


def create_user_table():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,  -- This is the email field
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
