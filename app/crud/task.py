import sqlite3

from app.utils.id_gen import get_id_str


def store_task(db: sqlite3.Connection, title, status, content, board_id, user_id):
    cursor = db.cursor()

    task_id = get_id_str()

    cursor.execute("INSERT INTO tasks (task_id, title, status, content, board_id, created_by) VALUES (?, ?, ?, ?, ?, ?)", (
        task_id, title, status, content, board_id, user_id),
    )
    db.commit()

    return task_id


def get_tasks_for_board(db: sqlite3.Connection, board_id, user_id):
    tasks = db.execute(
        """
        SELECT t.task_id, t.title, t.status, t.content, t.board_id, t.created_by, t.created_at
        FROM tasks t
        JOIN board_users bu ON t.board_id = bu.board_id
        WHERE bu.board_id = ? AND bu.user_id = ?
        """, (board_id, user_id),
    ).fetchall()

    return [dict(task) for task in tasks]


def update_task_details(db: sqlite3.Connection, task_id, title=None, status=None, content=None):
    cursor = db.cursor()

    # https://www.reddit.com/r/golang/comments/8875n4/partial_updates_with_databasesql_is_this_possible/
    cursor.execute(
        """
        UPDATE tasks
        SET title = COALESCE(?, title), status = COALESCE(?, status), content = COALESCE(?, content)
        WHERE task_id = ?
    """, (title, status, content, task_id))
    db.commit()
