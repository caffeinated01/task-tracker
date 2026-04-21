from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from pwdlib import PasswordHash

from flask import current_app

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=current_app.config['ACCESS_TOKEN_EXPIRE_MINUTES'])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, current_app.config['ACCESS_TOKEN_SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])
    return encoded_jwt


def create_refresh_token(data, expires_delta=None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=current_app.config['REFRESH_TOKEN_EXPIRE_DAYS']
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, current_app.config['REFRESH_TOKEN_SECRET_KEY'], algorithm=current_app.config['ALGORITHM']
    )

    return encoded_jwt, expire


def decode_refresh_token(refresh_token):
    try:
        data = jwt.decode(
            refresh_token,
            current_app.config["REFRESH_TOKEN_SECRET_KEY"],
            algorithms=[current_app.config["ALGORITHM"]]
        )
        return data

    except JWTError:
        return None
