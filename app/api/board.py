from flask import Blueprint, g, jsonify, request

from app.db import get_db
from app.utils.decorators import access_token_required, json_required
from app.crud.board import store_board, get_boards_for_user, get_board_by_id_for_user, check_user_in_board
from app.crud.task import get_tasks_for_board, store_task

bp = Blueprint('board', __name__, url_prefix='/api/boards')


@bp.route("/", methods=["GET"])
@access_token_required
def fetch_boards():
    db = get_db()
    user_id = g.current_user["id"]

    boards = get_boards_for_user(db, user_id)
    return jsonify(boards)


@bp.route("/", methods=["POST"])
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


@bp.route("/<int:id>", methods=["GET"])
@access_token_required
def fetch_board(id):
    user_id = g.current_user["id"]

    db = get_db()
    board = get_board_by_id_for_user(db, id, user_id)

    if not board:
        return jsonify({"message": "Board not found"}), 404

    return jsonify(board)


@bp.route("/<int:id>/tasks", methods=["GET"])
@access_token_required
def fetch_tasks_for_board(id):
    user_id = g.current_user["id"]

    db = get_db()
    tasks = get_tasks_for_board(db, id, user_id)

    return jsonify(tasks)


@bp.route("/<int:id>/tasks", methods=["POST"])
@access_token_required
@json_required
def create_task_for_board(id, data):
    user_id = g.current_user["id"]

    db = get_db()

    if check_user_in_board(db, id, user_id):
        return jsonify({"message": "User does not have access to this board"}), 403

    title, status, content = data.get(
        "title"), data.get("status"), data.get("content")

    if not title:
        return jsonify({"message": "Missing title"}), 400
    if not status:
        return jsonify({"message": "Missing status"}), 400
    if not content:
        return jsonify({"message": "Missing content"}), 400

    task_id = store_task(db, title, status, content, id, user_id)

    return {"id": task_id, "title": title, "status": status, "content": content, "board_id": id, "created_by": user_id}, 201


@bp.route("/", methods=["PATCH"])
@access_token_required
def update_board():
    return


@bp.route("/", methods=["DELETE"])
@access_token_required
def delete_board():
    return
