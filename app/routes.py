from flask import Blueprint, g, request, jsonify, render_template, redirect, url_for, make_response, current_app
from functools import wraps
from jose import jwt, JWTError
import sqlite3

from app.db import get_db
from app.utils.auth import create_access_token, get_password_hash, verify_password

bp = Blueprint('routes', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token, current_app.config['ACCESS_TOKEN_SECRET_KEY'], algorithms=[
                    current_app.config['ALGORITHM']]
            )
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?", (data["sub"],))
            current_user = cursor.fetchone()
            if current_user is None:
                return jsonify({"message": "User not found"}), 401
            g.current_user = dict(current_user)
        except JWTError:
            return jsonify({"message": "Token is invalid!"}), 401
        except Exception as e:
            return jsonify({"message": str(e)}), 500

        return f(*args, **kwargs)
    return decorated


@bp.route("/health")
def health():
    return "OK"


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/profile")
@token_required
def profile():
    username = g.current_user["username"]
    return f"Hello, {username}!"


@bp.route("/boards")
@token_required
def boards():
    return render_template("boards.html")


@bp.route("/signup")
def signup():
    return render_template("signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
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

    return redirect(url_for("routes.login"))


@bp.route("/login")
def login():
    return render_template("login.html")


@bp.route("/login", methods=["POST"])
def login_post():
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

    response = redirect(url_for("routes.boards"))
    response.set_cookie("access_token", access_token, httponly=True)
    return response


@bp.route("/logout")
def logout():
    response = make_response(redirect(url_for("routes.index")))
    response.set_cookie("access_token", "", expires=0)
    return response


@bp.route("/api/task/create", methods=["POST"])
@token_required
def create_task():
    return


@bp.route("/api/task/update", methods=["POST"])
@token_required
def update_task():
    return


@bp.route("/api/task/delete", methods=["POST"])
@token_required
def delete_task():
    return
