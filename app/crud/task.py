import sqlite3


def store_task(db: sqlite3.Connection, title, status, content, board_id, user_id):
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (title, status, content, board_id, created_by) VALUES (?, ?, ?, ?)", (
        title, status, content, board_id, user_id),
    )
    db.commit()
    return cursor.lastrowid


def get_tasks_for_board(db: sqlite3.Connection, board_id, user_id):
    tasks = db.execute(
        """
        SELECT t.id, t.title, t.status, t.content, t.board_id, t.created_by, t.created_at
        FROM tasks t
        JOIN board_users bu ON t.board_id = bu.board_id
        WHERE bu.board_id = ? AND bu.user_id = ?
        """, (board_id, user_id),
    ).fetchall()

    return [dict(task) for task in tasks]
