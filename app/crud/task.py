import sqlite3

from app.utils.id_gen import get_id_str


def store_task(db: sqlite3.Connection, title, status, content, importance, board_id, user_id, assigned_to=None):
    task_id = get_id_str()

    db.execute("INSERT INTO tasks (task_id, title, status, content, importance, board_id, created_by, assigned_to) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
        task_id, title, status, content, importance, board_id, user_id, assigned_to),
    )
    db.commit()

    return task_id


def get_task_by_id_for_user(db: sqlite3.Connection, task_id, user_id):
    task = db.execute(
        """
        SELECT t.task_id, t.title, t.status, t.content, t.importance, t.board_id, u.username AS created_by, t.assigned_to, t.created_at
        FROM tasks t
        JOIN users u ON t.created_by = u.user_id
        JOIN board_users bu ON t.board_id = bu.board_id
        WHERE t.task_id = ? AND bu.user_id = ?
        """, (task_id, user_id),
    ).fetchone()

    return dict(task) if task else None


def get_tasks_for_board(db: sqlite3.Connection, board_id, user_id):
    tasks = db.execute(
        """
        SELECT t.task_id, t.title, t.status, t.content, t.importance, t.board_id, u.username AS created_by, t.assigned_to, t.created_at
        FROM tasks t
        JOIN users u ON t.created_by = u.user_id
        JOIN board_users bu ON t.board_id = bu.board_id
        WHERE bu.board_id = ? AND bu.user_id = ?
        """, (board_id, user_id),
    ).fetchall()

    return [dict(task) for task in tasks]


def update_task_details(db, task_id, data):
    fields = []
    values = []

    for key in ["title", "status", "content", "importance", "assigned_to"]:
        if key in data:
            fields.append(f"{key} = ?")
            values.append(data[key])

    if not fields:
        return

    values.append(task_id)

    db.execute(
        f"""
        UPDATE tasks
        SET {", ".join(fields)}
        WHERE task_id = ?
        """,
        values,
    )

    db.commit()


def delete_task(db: sqlite3.Connection, task_id):
    db.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    db.commit()
