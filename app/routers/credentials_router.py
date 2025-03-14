
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database

from api_models.credentials import RecoveryCreateModel, ResetCreateModel
from services.email_service import send_recovery_email
from services.credentials_service import post_recovery_password, reset_password
from core.response_helper import send_response

router = APIRouter()

@router.post("/recovery")
def recovery(
    recovery_data: RecoveryCreateModel,

    db: Session = Depends(database.get_db)
):
    plain_password = post_recovery_password(db, recovery_data.email)

    send_recovery_email(recovery_data.email, plain_password)
    
    return send_response(
        "Contraseña asignada correctamente",
        200,
    )

@router.post("/reset/{profile_id}")
def reset(
    profile_id: str,
    recovery_data: ResetCreateModel,
    db: Session = Depends(database.get_db)
):
    reset_password(db, profile_id, recovery_data.password)

    return send_response(
        "Contraseña reasignada correctamente",
        200,
    )

