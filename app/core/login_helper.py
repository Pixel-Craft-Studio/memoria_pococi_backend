from core.response_helper import send_response
import bcrypt
import jwt

from datetime import datetime, timedelta, timezone
from core.config import settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(plain_password):
    password = plain_password.encode("utf-8")
    pepper = settings.pepper.encode("utf-8")

    combined_password = password + pepper
    hashed_password = bcrypt.hashpw(combined_password, bcrypt.gensalt())

    return hashed_password.decode("utf-8")


def verify_password(input_password, stored_hash):
    combined_input = input_password.encode("utf-8") + settings.pepper.encode("utf-8")
    return bcrypt.checkpw(combined_input, stored_hash.encode("utf-8"))


def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(
        hours=settings.access_token_expire_hours
    )
    payload = data.copy()
    payload.update({"exp": expire})

    return jwt.encode(
        payload, settings.api_secret_key, algorithm=settings.secret_algorithm
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.api_secret_key, algorithms=[settings.secret_algorithm])

        token_exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)

        if token_exp - now < timedelta(minutes=5):
            new_token = create_access_token(data={"sub": payload["sub"]})
            return {"detail": "Token is valid", "access_token": new_token}

        return {"detail": "El token es válido"}
    except jwt.ExpiredSignatureError:
        raise Exception("El token ha expirado")
    except jwt.InvalidTokenError:
        raise Exception("El token es inválido")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.api_secret_key, algorithms=[settings.secret_algorithm]
        )
        user: str = payload.get("sub")
        if user is None:
            return send_response(
                "No se pudieron validar las credenciales", status_code=401
            )

        return user

    except jwt.PyJWTError:
        return send_response("No se pudieron validar las credenciales", status_code=401)
