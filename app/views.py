from flask import Blueprint, render_template, g
from app.utils.decorators import token_required

bp = Blueprint('views', __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/health")
def health():
    return "OK"


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


@bp.route("/login")
def login():
    return render_template("login.html")
