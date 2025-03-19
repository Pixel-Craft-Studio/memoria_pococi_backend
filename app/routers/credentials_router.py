from datetime import datetime, timezone
from services.profile_service import get_one_profile
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database

from api_models.credentials import RecoveryCreateModel, ResetCreateModel
from services.email_service import send_recovery_email
from services.credentials_service import post_recovery_password, reset_password
from services.credentials_service import delete_recovery_by_id, get_recovery_by_id
from core.response_helper import send_response
from core.login_helper import create_access_token, verify_password


router = APIRouter()


@router.post("/recovery")
def recovery(
    recovery_data: RecoveryCreateModel, db: Session = Depends(database.get_db)
):
    plain_password = post_recovery_password(db, recovery_data.email)

    if not plain_password:
        return send_response("Surgió un error al generar la contraseña", status_code=400)

    send_recovery_email(recovery_data.email, plain_password)

    return send_response(
        "Contraseña asignada correctamente",
        200,
    )


@router.post("/reset")
def reset(recovery_data: ResetCreateModel, db: Session = Depends(database.get_db)):
    profile = get_one_profile(db=db, profile_id=recovery_data.profile_id)

    if not profile:
        return send_response("El perfil no fue encontrado", status_code=400)

    recovery = None
    if verify_password(recovery_data.currentPassword, profile.password_hash):
        isValidPassword = True
    else:
        recovery = get_recovery_by_id(db, recovery_data.profile_id)
        if recovery and recovery.expiration < datetime.now(timezone.utc):
            delete_recovery_by_id(db, profile.id)
            recovery = None

        isValidPassword = recovery and verify_password(
            recovery_data.currentPassword, recovery.password
        )

    if not isValidPassword:
        return send_response("Credenciales incorrectas", status_code=401)

    reset_password(db, recovery_data.profile_id, recovery_data.password)
    access_token = create_access_token(data={"sub": profile.to_response_dict()})

    return send_response(
        "Contraseña reasignada correctamente", {"access_token": access_token}, 200
    )
