from flask import Blueprint, g, jsonify

from app.db import get_db
from app.utils.decorators import access_token_required, json_required
from app.crud.board import store_board, get_boards_for_user, get_board_by_id_for_user

bp = Blueprint('board', __name__, url_prefix='/api/board')


@bp.route("/boards", methods=["GET"])
@access_token_required
def fetch_boards():
    db = get_db()
    user_id = g.current_user["id"]

    boards = get_boards_for_user(db, user_id)
    return jsonify(boards)


@bp.route("/create", methods=["POST"])
@access_token_required
@json_required
def create_board(data):
    user_id = g.current_user["id"]
    board_name = data.get("name")

    if not board_name:
        return jsonify({"message": "Missing name"}), 400

    db = get_db()
    board_id = store_board(db, board_name, user_id)
    return jsonify({"id": board_id, "name": board_name}), 201


@bp.route("/board/<int:id>", methods=["GET"])
@access_token_required
def fetch_board(id):
    user_id = g.current_user["id"]

    db = get_db()
    board = get_board_by_id_for_user(db, id, user_id)

    if not board:
        return jsonify({"message": "Board not found"}), 404

    return jsonify(board)


@bp.route("/update", methods=["POST"])
@access_token_required
def update_board():
    return


@bp.route("/delete", methods=["POST"])
@access_token_required
def delete_board():
    return
