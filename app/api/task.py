from flask import Blueprint

from app.utils.decorators import access_token_required


bp = Blueprint('task', __name__, url_prefix='/api/tasks')


@bp.route("/<int:id>", methods=["GET"])
@access_token_required
def fetch_task(id):
    return


@bp.route("/<int:id>", methods=["PATCH"])
@access_token_required
def update_task(id):
    return


@bp.route("/<int:id>", methods=["DELETE"])
@access_token_required
def delete_task(id):
    return
