import sqlite3

# Hinglish: Ye database connection banata hai

def get_connection():
    conn = sqlite3.connect("chat.db")
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()