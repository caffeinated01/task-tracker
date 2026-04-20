from flask import Blueprint
from app.utils.decorators import token_required

bp = Blueprint('task', __name__, url_prefix='/api/task')


@bp.route("/create", methods=["POST"])
@token_required
def create_task():
    return


@bp.route("/update", methods=["POST"])
@token_required
def update_task():
    return


@bp.route("/delete", methods=["POST"])
@token_required
def delete_task():
    return
