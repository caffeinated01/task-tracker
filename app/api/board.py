from flask import Blueprint, g, jsonify, request

from app.db import get_db
from app.utils.decorators import access_token_required, json_required
from app.constants import BoardRole
from app.crud.board import store_board, get_boards_for_user, get_board_by_id_for_user, check_user_in_board, add_user_to_board, remove_user_from_board, get_users_for_board, update_board_name, remove_board
from app.crud.task import get_tasks_for_board, store_task
from app.crud.user import get_user_by_username, get_user_by_id

bp = Blueprint('board', __name__, url_prefix='/api/boards')


@bp.route("/", methods=["GET"])
@access_token_required
def fetch_boards():
    db = get_db()
    user_id = g.current_user["user_id"]

    boards = get_boards_for_user(db, user_id)

    user = get_user_by_id(db, user_id)

    res = {
        "boards": boards,
        "user": {
            "username": user["username"],
            "user_id": user_id
        }
    }

    return jsonify(res)


@bp.route("/", methods=["POST"])
@access_token_required
@json_required
def create_board(data):
    user_id = g.current_user["user_id"]
    board_name = data.get("name")

    if not board_name:
        return jsonify({"message": "Missing name"}), 400

    db = get_db()
    board_id = store_board(db, board_name, user_id)
    return jsonify({"id": board_id, "name": board_name}), 201


@bp.route("/<string:id>", methods=["GET"])
@access_token_required
def fetch_board(id):
    user_id = g.current_user["user_id"]

    db = get_db()
    board = get_board_by_id_for_user(db, id, user_id)

    if not board:
        return jsonify({"message": "Board not found"}), 404

    user = get_user_by_id(db, user_id)
    res = {
        "board": board,
        "user": {
            "username": user["username"],
            "user_id": user_id
        }
    }
    return jsonify(res)


@bp.route("/<string:id>", methods=["PATCH"])
@access_token_required
@json_required
def update_board(id, data):
    user_id = g.current_user["user_id"]
    name = data.get("name")

    if not name:
        return jsonify({"message": "Missing name"}), 400

    db = get_db()

    board = get_board_by_id_for_user(db, id, user_id)

    if not board:
        return jsonify({"message": "Board not found"}), 404

    if board["role"] != BoardRole.OWNER:
        return jsonify({"message": "Only the owner of the board can update it"}), 403

    update_board_name(db, id, name)

    return jsonify({"message": "Board updated successfully"})


@bp.route("/<string:id>", methods=["DELETE"])
@access_token_required
def delete_board(id):
    user_id = g.current_user["user_id"]

    db = get_db()

    board = get_board_by_id_for_user(db, id, user_id)

    if not board:
        return jsonify({"message": "Board not found"}), 404

    if board["role"] != BoardRole.OWNER:
        return jsonify({"message": "Only the owner of the board can delete it"}), 403

    remove_board(db, id)

    return jsonify({"message": "Board deleted successfully"})


@bp.route("/<string:id>/tasks", methods=["GET"])
@access_token_required
def fetch_tasks_for_board(id):
    user_id = g.current_user["user_id"]
    db = get_db()
    tasks = get_tasks_for_board(db, id, user_id)

    return jsonify(tasks)


@bp.route("/<string:id>/tasks", methods=["POST"])
@access_token_required
@json_required
def create_task_for_board(id, data):
    user_id = g.current_user["user_id"]

    db = get_db()

    if not check_user_in_board(db, id, user_id):
        return jsonify({"message": "You don't have access to this board"}), 403

    title, status, content, importance, assigned_to = data.get("title"), data.get(
        "status"), data.get("content"), data.get("importance"), data.get("assigned_to")

    if not title:
        return jsonify({"message": "Missing title"}), 400
    if not status:
        return jsonify({"message": "Missing status"}), 400
    if not content:
        return jsonify({"message": "Missing content"}), 400
    if not importance:
        return jsonify({"message": "Missing importance"}), 400

    task_id = store_task(db, title, status, content,
                         importance, id, user_id, assigned_to)

    return jsonify({"id": task_id, "title": title, "status": status, "content": content, "importance": importance, "board_id": id, "created_by": user_id, "assigned_to": assigned_to}), 201


@bp.route("/<string:id>/users", methods=["GET"])
@access_token_required
def fetch_board_users(id):
    user_id = g.current_user["user_id"]

    db = get_db()

    if not check_user_in_board(db, id, user_id):
        return jsonify({"message": "You don't have access to this board"}), 403

    users = get_users_for_board(db, id)
    return jsonify(users)


@bp.route("/<string:id>/users", methods=["POST"])
@access_token_required
@json_required
def share_board(id, data):
    user_id = g.current_user["user_id"]

    db = get_db()

    board = get_board_by_id_for_user(db, id, user_id)

    if not board:
        return jsonify({"message": "Board not found"}), 404

    if board["role"] != BoardRole.OWNER:
        return jsonify({"message": "Only the owner of the board can share it"}), 403

    username_to_share_with = data.get("username")

    if not username_to_share_with:
        return jsonify({"message": "Missing username"}), 400

    user_to_share_with = get_user_by_username(db, username_to_share_with)

    if not user_to_share_with:
        return jsonify({"message": f"User not found"}), 404

    user_id_to_share_with = user_to_share_with["user_id"]

    if user_id_to_share_with == user_id:
        return jsonify({"message": "Can't share board with yourself"}), 400

    if check_user_in_board(db, id, user_id_to_share_with):
        return jsonify({"message": f"Board is already shared with user"}), 409

    add_user_to_board(db, id, user_id_to_share_with)

    return jsonify({"message": f"Board shared with {username_to_share_with}"})


@bp.route("/<string:id>/users/<string:user_id_to_revoke>", methods=["DELETE"])
@access_token_required
def revoke_board_access(id, user_id_to_revoke):
    user_id = g.current_user["user_id"]

    db = get_db()

    board = get_board_by_id_for_user(db, id, user_id)

    if not board:
        return jsonify({"message": "Board not found"}), 404

    if board["role"] != BoardRole.OWNER:
        return jsonify({"message": "Only the owner of the board can revoke access"}), 403

    user_to_revoke = get_user_by_id(db, user_id_to_revoke)

    if not user_to_revoke:
        return jsonify({"message": f"User not found"}), 404

    if user_id_to_revoke == user_id:
        return jsonify({"message": "Can't revoke your own access from board"}), 400

    if not check_user_in_board(db, id, user_id_to_revoke):
        return jsonify({"message": f"User not in board"}), 404

    username_to_revoke = user_to_revoke["username"]

    remove_user_from_board(db, id, user_id_to_revoke)

    return jsonify({"message": f"Access revoked for {username_to_revoke}"})
