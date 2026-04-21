from datetime import timedelta

from flask import Blueprint, current_app, jsonify, request, redirect, url_for, make_response

from app.crud.token import revoke_refresh_token, rotate_refresh_token, store_refresh_token
from app.crud.user import create_user, get_user_by_username
from app.db import get_db
from app.utils.auth import create_access_token, get_password_hash, verify_password

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password", 400

    db = get_db()

    if get_user_by_username(db, username):
        return "Username already exists", 409

    hashed_password = get_password_hash(password)

    create_user(db, username, hashed_password)

    return redirect(url_for("views.login"))


@bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password", 400

    db = get_db()

    user = get_user_by_username(db, username)

    if not user or not verify_password(password, user["hashed_password"]):
        return "Incorrect username or password", 401

    access_token = create_access_token(data={"sub": str(user["id"])})
    refresh_token = store_refresh_token(db, user)

    response = redirect(url_for("views.boards"))
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return response


@bp.route("/refresh", methods=["POST"])
def refresh_accesss_token():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return "Refresh token is missing!", 401

    db = get_db()

    new_refresh_token, user = rotate_refresh_token(db, refresh_token)

    new_access_token = create_access_token(
        data={"sub": str(user["id"])},
        expires_delta=timedelta(
            minutes=current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"])
    )

    response = jsonify({"access_token": new_access_token})
    response.set_cookie("access_token", new_access_token, httponly=True)
    response.set_cookie("refresh_token", new_refresh_token, httponly=True)

    return response


@bp.route("/logout")
def logout():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return "Refresh token is missing!", 401

    db = get_db()

    revoke_refresh_token(db, refresh_token)

    response = make_response(redirect(url_for("views.index")))
    response.set_cookie("access_token", "", expires=0)
    response.set_cookie("refresh_token", "", expires=0)
    return response
