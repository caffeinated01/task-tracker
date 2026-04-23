import sqlite3


def store_board(db: sqlite3.Connection, name, owner_id):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO boards (name, owner_id) VALUES (?, ?)", (name, owner_id))
    board_id = cursor.lastrowid  # get auto generated id from insert
    cursor.execute("INSERT INTO board_users (user_id, board_id, role) VALUES (?, ?, ?)",
                   (owner_id, board_id, "owner"))
    db.commit()
    return board_id


def get_boards_for_user(db: sqlite3.Connection, user_id):
    boards = db.execute(
        """
        SELECT b.id, b.name, bu.role
        FROM boards b
        JOIN board_users bu ON b.id = bu.board_id
        WHERE bu.user_id = ?
        """, (user_id,)
    ).fetchall()

    return [dict(board) for board in boards]


def get_board_by_id_for_user(db: sqlite3.Connection, board_id, user_id):
    board = db.execute(
        """
        SELECT b.id, b.name, bu.role
        FROM boards b
        JOIN board_users bu ON b.id = bu.board_id
        WHERE b.id = ? AND bu.user_id = ?
        """,
        (board_id, user_id)
    ).fetchone()

    return dict(board) if board else None


def check_user_in_board(db: sqlite3.Connection, board_id, user_id):
    membership = db.execute(
        "SELECT * FROM board_users WHERE board_id = ? AND user_id = ?", (
            board_id, user_id)
    ).fetchone()

    return membership is not None


def add_user_to_board(db: sqlite3.Connection, board_id, user_id, role="member"):
    db.execute("INSERT INTO board_users (user_id, board_id, role) VALUES (?, ?, ?)",
               (user_id, board_id, role))
    db.commit()


def remove_user_from_board(db: sqlite3.Connection, board_id, user_id):
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM board_users WHERE board_id = ? AND user_id = ?", (board_id, user_id))
    db.commit()


def get_users_for_board(db: sqlite3.Connection, board_id):
    users = db.execute(
        """
        SELECT u.id, u.username, bu.role
        FROM users u
        JOIN board_users bu ON u.id = bu.user_id
        WHERE bu.board_id = ?
        """, (board_id,)
    ).fetchall()

    return [dict(user) for user in users]
