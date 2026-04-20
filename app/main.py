import sqlite3
from functools import wraps
from flask import Flask, g, request, make_response, render_template, jsonify, redirect, url_for
from jose import jwt, JWTError

from app.utils.auth import create_access_token, get_password_hash, verify_password

from app.config import settings

app = Flask(__name__)


app.config.from_mapping(
    DATABASE="database.db",
)


def init_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    with app.open_resource("schema.sql") as f:
        conn.executescript(f.read().decode("utf8"))
    conn.commit()
    conn.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[
                    settings.ALGORITHM]
            )
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM user WHERE username = ?", (data["sub"],))
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


@app.route("/health")
def health():
    return "OK"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
@token_required
def profile():
    username = g.current_user["username"]
    return f"Hello, {username}!"


@app.route("/board")
@token_required
def board():
    return render_template("board.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
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
            "INSERT INTO user (username, hashed_password) VALUES (?, ?)",
            (username, hashed_password),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return "Username already exists", 409

    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password", 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user or not verify_password(password, user["hashed_password"]):
        return "Incorrect username or password", 401

    access_token = create_access_token(data={"sub": user["username"]})

    response = redirect(url_for("board"))
    response.set_cookie("access_token", access_token, httponly=True)
    return response


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("index")))
    response.set_cookie("access_token", "", expires=0)
    return response


@app.route("/api/task/create", methods=["POST"])
@token_required
def create_task():
    return


@app.route("/api/task/update", methods=["POST"])
@token_required
def update_task():
    return


@app.route("/api/task/delete", methods=["POST"])
@token_required
def delete_task():
    return


if __name__ == "__main__":
    init_db()
    app.run()
