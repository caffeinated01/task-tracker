from datetime import datetime
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

from flask import abort, make_response, jsonify

from app.utils.auth import create_refresh_token, decode_refresh_token


def store_refresh_token(db: sqlite3.Connection, user):
    refresh_token, expires_at = create_refresh_token(data={
        "sub": user["user_id"],
        "jti": str(uuid4())
    })

    cursor = db.cursor()
    cursor.execute("INSERT INTO refresh_tokens (token, expires_at, user_id) VALUES (?, ?, ?)",
                   (refresh_token, expires_at, user["user_id"]))
    db.commit()

    return refresh_token


def rotate_refresh_token(db: sqlite3.Connection, refresh_token):
    cursor = db.cursor()

    data = decode_refresh_token(refresh_token)

    if not data:
        # invalid token
        abort(make_response(jsonify(message="Could not validate credentials"), 401))

    token = cursor.execute(
        "SELECT * FROM refresh_tokens WHERE token = ?", (refresh_token,)).fetchone()

    if not token or token["revoked_at"] is not None:
        # no token found or token revoked
        abort(make_response(jsonify(message="Could not validate credentials"), 401))

    token_expires_at = token["expires_at"]

    if token_expires_at.tzinfo is None:
        token_expires_at = token_expires_at.replace(tzinfo=timezone.utc)

    if token_expires_at < datetime.now(timezone.utc):
        # token expired
        abort(make_response(jsonify(message="Could not validate credentials"), 401))

    revoke_refresh_token(db, refresh_token)

    user_id = data["sub"]
    user = cursor.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if not user:
        # user not found
        abort(make_response(jsonify(message="Could not validate credentials"), 401))

    new_refresh_token = store_refresh_token(db, user)

    db.commit()

    return new_refresh_token, user


def revoke_refresh_token(db: sqlite3.Connection, refresh_token):
    cursor = db.cursor()

    token = cursor.execute(
        "SELECT * FROM refresh_tokens WHERE token = ?", (refresh_token,)).fetchone()

    if not token or token["revoked_at"] is not None:
        # no token found or token revoked
        abort(make_response(jsonify(message="Could not validate credentials"), 401))

    revoked_at = datetime.now(timezone.utc)
    cursor.execute("UPDATE refresh_tokens SET revoked_at = ? WHERE id = ?",
                   (revoked_at, token["id"]))
    db.commit()
