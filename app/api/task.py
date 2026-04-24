from flask import Blueprint, g, jsonify

from app.db import get_db
from app.crud.board import get_board_by_task_id_for_user, check_user_in_board
from app.crud.task import update_task_details
from app.utils.decorators import access_token_required, json_required


bp = Blueprint('task', __name__, url_prefix='/api/tasks')


@bp.route("/<string:id>", methods=["GET"])
@access_token_required
def fetch_task(id):
    return


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

    # if field is empty then the new value will be None.
    # we use COALESCE in update_task_details to keep the old value if the new value is None
    new_title = data.get("title")
    new_status = data.get("status")
    new_content = data.get("content")

    update_task_details(db, id, new_title, new_status, new_content)

    return jsonify({"message": "Task updated successfully"}), 200


@bp.route("/<string:id>", methods=["DELETE"])
@access_token_required
def delete_task(id):
    return
