from flask import Blueprint, request, redirect, url_for, make_response
import sqlite3

from app.db import get_db
from app.utils.auth import create_access_token, get_password_hash, verify_password

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password", 400

    hashed_password = get_password_hash(password)

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (username, hashed_password),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return "Username already exists", 409

    return redirect(url_for("views.login"))


@bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password", 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user or not verify_password(password, user["hashed_password"]):
        return "Incorrect username or password", 401

    access_token = create_access_token(data={"sub": user["username"]})

    response = redirect(url_for("views.boards"))
    response.set_cookie("access_token", access_token, httponly=True)
    return response


@bp.route("/logout")
def logout():
    response = make_response(redirect(url_for("views.index")))
    response.set_cookie("access_token", "", expires=0)
    return response
