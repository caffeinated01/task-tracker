from app.crud.task import delete_task, get_task_by_id_for_user, update_task_details, get_tasks_assigned_to_user
from flask import Blueprint, g, jsonify

from app.db import get_db
from app.utils.decorators import access_token_required, json_required
from app.crud.board import get_board_by_task_id_for_user, check_user_in_board
from app.crud.task import delete_task, get_task_by_id_for_user, update_task_details


bp = Blueprint('task', __name__, url_prefix='/api/tasks')


@bp.route("/<string:id>", methods=["GET"])
@access_token_required
def fetch_task(id):
    user_id = g.current_user["user_id"]

    db = get_db()

    task = get_task_by_id_for_user(db, id, user_id)

    return jsonify(task)


@bp.route("/<string:id>", methods=["PATCH"])
@access_token_required
@json_required
def update_task(id, data):
    user_id = g.current_user["user_id"]

    db = get_db()

    board = get_board_by_task_id_for_user(db, id, user_id)
    board_id = board["board_id"]

    if not check_user_in_board(db, board_id, user_id):
        return {"message": "You don't have access to this task"}, 400

    update_task_details(db, id, data)

    return jsonify({"message": "Task updated successfully"}), 200


@bp.route("/<string:id>", methods=["DELETE"])
@access_token_required
def purge_task(id):
    user_id = g.current_user["user_id"]

    db = get_db()

    board = get_board_by_task_id_for_user(db, id, user_id)
    board_id = board["board_id"]

    if not check_user_in_board(db, board_id, user_id):
        return {"message": "You don't have access to this task"}, 400

    delete_task(db, id)

    return jsonify({"message": "Task deleted successfully"}), 200


@bp.route("/assigned", methods=["GET"])
@access_token_required
def fetch_assigned_tasks():
    user_id = g.current_user["user_id"]

    db = get_db()

    tasks = get_tasks_assigned_to_user(db, user_id)
    
    return jsonify(tasks)
