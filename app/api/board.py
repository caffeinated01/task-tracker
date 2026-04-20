from flask import Blueprint
from app.utils.decorators import token_required

bp = Blueprint('board', __name__, url_prefix='/api/board')


@bp.route("/create", methods=["POST"])
@token_required
def create_board():
    return


@bp.route("/update", methods=["POST"])
@token_required
def update_board():
    return


@bp.route("/delete", methods=["POST"])
@token_required
def delete_board():
    return
