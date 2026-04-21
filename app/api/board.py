from flask import Blueprint, g, jsonify

from app.utils.decorators import access_token_required

bp = Blueprint('board', __name__, url_prefix='/api/board')


@bp.route("/fetch", methods=["GET"])
@access_token_required
def fetch_boards():
    return jsonify({"boards": ["1", "2", "3"]})  # placeholder


@bp.route("/create", methods=["POST"])
@access_token_required
def create_board():
    return


@bp.route("/update", methods=["POST"])
@access_token_required
def update_board():
    return


@bp.route("/delete", methods=["POST"])
@access_token_required
def delete_board():
    return
