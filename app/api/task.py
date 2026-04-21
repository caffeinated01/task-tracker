from flask import Blueprint, jsonify
from app.utils.decorators import access_token_required

bp = Blueprint('task', __name__, url_prefix='/api/task')


@bp.route("/create", methods=["POST"])
@access_token_required
def create_task():
    return jsonify({"message": "Success"})


@bp.route("/update", methods=["POST"])
@access_token_required
def update_task():
    return


@bp.route("/delete", methods=["POST"])
@access_token_required
def delete_task():
    return
