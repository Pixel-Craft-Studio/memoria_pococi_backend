from core.response_helper import send_response
from services.profile_service import get_profile_by_email
from core.login_helper import create_access_token, decode_access_token, verify_password
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.login_helper import oauth2_scheme
from db import database


router = APIRouter()


@router.post("")
async def dashboard_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    username = form_data.username
    password = form_data.password

    profile = get_profile_by_email(db=db, email=username)

    if not profile:
        return send_response("Credenciales incorrectas", status_code=401)

    if not verify_password(password, profile.password_hash):
        return send_response("Credenciales incorrectas", status_code=401)

    access_token = create_access_token(data={"sub": profile.to_response_dict()})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/validate")
async def dashboard_validate_token(token: str):
    try:
        return decode_access_token(token)
    except Exception as e:
        return send_response(f"{e}", status_code=401)
