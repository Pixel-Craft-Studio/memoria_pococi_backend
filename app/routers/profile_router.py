
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from services.profile_service import (
    ProfileCreateModel,
    ProfileUpdateModel,
    create_profile,
    get_one_profile,
    get_all_profiles,
    update_profile,
    remove_profile,
)
from core.response_helper import send_response
from uuid import UUID

router = APIRouter()


@router.get("")
def get_profiles(
    db: Session = Depends(database.get_db)
):
    profiles = get_all_profiles(db=db)
    return send_response(
        "Perfiles obtenidos exitosamente",
        [profile.to_response_dict() for profile in profiles],
        200,
    )


@router.get("/{profile_id}")
def get_profile(
    profile_id: UUID,
    db: Session = Depends(database.get_db)
):
    profile = get_one_profile(db=db, profile_id=profile_id)
    if not profile:
        return send_response("Perfil no encontrado", status_code=404)
    return send_response(
        "Perfil obtenido exitosamente", profile.to_response_dict(), 200
    )


@router.post("")
def post_profile(
    profile: ProfileCreateModel,
    db: Session = Depends(database.get_db),
    
):
    try:
        created_profile = create_profile(db=db, profile=profile)

        return send_response(
            "Perfil creado exitosamente", created_profile.to_response_dict(), 201
        )

    except Exception as e:
        return send_response(f"{e}", status_code=404)


@router.patch("/{profile_id}")
def patch_profile(
    profile_id: UUID,
    profile_update: ProfileUpdateModel,
    db: Session = Depends(database.get_db),
):
    try:
        updated_profile = update_profile(
            db=db, profile_id=profile_id, profile_update=profile_update
        )
        return send_response(
            "Perfil actualizado exitosamente", updated_profile.to_response_dict(), 200
        )

    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/{profile_id}")
def delete_profile(
    profile_id: UUID,
    db: Session = Depends(database.get_db),
):
    success = remove_profile(db=db, profile_id=profile_id)
    if not success:
        return send_response("Perfil no encontrado", status_code=404)
    return send_response("Perfil eliminado exitosamente", status_code=200)
