from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.login_helper import oauth2_scheme
from db import database

from services.credentials_service import delete_recovery_by_id, get_recovery_by_id
from core.response_helper import send_response
from services.profile_service import get_profile_by_email
from core.login_helper import create_access_token, decode_access_token, verify_password

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

    if verify_password(password, profile.password_hash):
        access_token = create_access_token(data={"sub": profile.to_response_dict()})
        return {"access_token": access_token, "token_type": "bearer"} 

    recovery = get_recovery_by_id(db, profile.id)
    if recovery:
        if recovery.expiration < datetime.now(timezone.utc): 
            delete_recovery_by_id(db, profile.id)
        elif verify_password(password, recovery.password):
            access_token = create_access_token(data={"sub": profile.to_response_dict(), "isTemporal": True})
            return {"access_token": access_token, "token_type": "bearer"}

    return send_response("Credenciales incorrectas", status_code=401)


@router.get("/validate")
async def dashboard_validate_token(token: str):
    try:
        return decode_access_token(token)
    except Exception as e:
        return send_response(f"{e}", status_code=401)
