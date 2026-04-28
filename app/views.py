from flask import Blueprint, render_template, redirect

bp = Blueprint('views', __name__)


@bp.route("/")
def index():
    return redirect("/login")


@bp.route("/health")
def health():
    return "OK"


@bp.route("/boards")
def boards():
    return render_template("boards.html")


@bp.route("/boards/<string:board_id>")
def board(board_id):
    return render_template("board.html", board_id=board_id)


@bp.route("/signup")
def signup():
    return render_template("signup.html")


@bp.route("/login")
def login():
    return render_template("login.html")
