import sqlite3
import re

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            gender TEXT,
            birthdate TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


def is_valid_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def register_db(username, password, gender, birthdate):

    if not is_valid_email(username):
        return "Invalid email format"

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        conn.close()
        return "Akun sudah terdaftar, silahkan lakukan login"

    c.execute("""
        INSERT INTO users (username, password, gender, birthdate, score)
        VALUES (?, ?, ?, ?, ?)
    """, (username, password, gender, birthdate,0))

    conn.commit()
    conn.close()

    return "Success"