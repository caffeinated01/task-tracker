import sqlite3


def get_user_by_username(db: sqlite3.Connection, username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

    return cursor.fetchone()


def create_user(db: sqlite3.Connection, username, hashed_password):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
        (username, hashed_password),
    )
    db.commit()
