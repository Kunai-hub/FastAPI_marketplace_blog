from datetime import datetime, timedelta

from jose import jwt, JWTError

from src.fastapi_marketplace_blog.core.config import config


def create_access_token(data: dict, method: str = "access"):
    to_encode = data.copy()
    expire = 0

    if method == "access":
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    elif method == "refresh":
        expire = datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str):
    try:
        decode = jwt.decode(
            token=token, key=config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        return decode
    except JWTError:
        return None
