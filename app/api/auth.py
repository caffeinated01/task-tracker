from datetime import timedelta

from flask import Blueprint, current_app, jsonify, request

from app.crud.token import revoke_refresh_token, rotate_refresh_token, store_refresh_token
from app.crud.user import create_user, get_user_by_username
from app.db import get_db
from app.utils.decorators import json_required
from app.utils.auth import create_access_token, get_password_hash, verify_password

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route("/signup", methods=["POST"])
@json_required
def signup(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    db = get_db()

    if get_user_by_username(db, username):
        return jsonify({"message": "Username already exists"}), 409

    hashed_password = get_password_hash(password)

    create_user(db, username, hashed_password)

    response = jsonify({"message": "Signup successful"}), 201
    return response


@bp.route("/login", methods=["POST"])
@json_required
def login(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    db = get_db()

    user = get_user_by_username(db, username)

    if not user or not verify_password(password, user["hashed_password"]):
        return jsonify({"message": "Incorrect username or password"}), 401

    access_token = create_access_token(data={"sub": str(user["id"])})
    refresh_token = store_refresh_token(db, user)

    response = jsonify({
        "message": "Login successful",
        "user": {"id": user["id"], "username": user["username"]}
    })
    response.set_cookie("access_token", access_token,
                        httponly=True, samesite="Lax")
    response.set_cookie("refresh_token", refresh_token,
                        httponly=True, samesite="Lax")
    return response


@bp.route("/refresh", methods=["POST"])
def refresh_access_token():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({"message": "Refresh token is missing!"}), 401

    db = get_db()

    new_refresh_token, user = rotate_refresh_token(db, refresh_token)

    new_access_token = create_access_token(
        data={"sub": str(user["id"])},
        expires_delta=timedelta(
            minutes=current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"])
    )

    response = jsonify({"access_token": new_access_token})
    response.set_cookie("access_token", new_access_token,
                        httponly=True, samesite="Lax")
    response.set_cookie("refresh_token", new_refresh_token,
                        httponly=True, samesite="Lax")

    return response


@bp.route("/logout")
def logout():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({"message": "Refresh token is missing!"}), 401

    db = get_db()

    revoke_refresh_token(db, refresh_token)

    response = jsonify({"message": "Logout successful"})
    response.set_cookie("access_token", "", expires=0, samesite="Lax")
    response.set_cookie("refresh_token", "", expires=0, samesite="Lax")
    return response
