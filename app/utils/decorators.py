from functools import wraps
from flask import request, jsonify, g, current_app
from jose import jwt, JWTError

from app.db import get_db


def access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token, current_app.config['ACCESS_TOKEN_SECRET_KEY'], algorithms=[
                    current_app.config['ALGORITHM']]
            )
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE id = ?", (data["sub"],))
            current_user = cursor.fetchone()
            if current_user is None:
                return jsonify({"message": "User not found"}), 401
            g.current_user = dict(current_user)
        except JWTError:
            return jsonify({"message": "Token is invalid!"}), 401
        except Exception as e:
            return jsonify({"message": str(e)}), 500

        return f(*args, **kwargs)
    return decorated
