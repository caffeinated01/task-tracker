import sqlite3

from app.utils.id_gen import get_id_str


def get_user_by_username(db: sqlite3.Connection, username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

    return cursor.fetchone()


def get_user_by_id(db: sqlite3.Connection, user_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))

    return cursor.fetchone()


def create_user(db: sqlite3.Connection, username, hashed_password):
    cursor = db.cursor()

    user_id = get_id_str()

    cursor.execute(
        "INSERT INTO users (user_id, username, hashed_password) VALUES (?, ?, ?)",
        (user_id, username, hashed_password)
    )
    db.commit()
