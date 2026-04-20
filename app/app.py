import sqlite3
from flask import Flask, g, request, render_template

app = Flask(__name__)


DATABASE = "data.db"


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@app.route("/health")
def health():
    return "OK"


@app.route("/")
def index():
    return render_template("index.html")

# auth routes


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    if request.method == "POST":
        # register here
        return


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    if request.method == "POST":
        # login here, return token ()
        return


@app.route("/logout")
def logout():
    # logout here
    return


if __name__ == "__main__":
    app.run()
