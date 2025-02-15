from core.validate_helper import validate_uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from services.social_platform_service import (
    SocialPlatformCreateModel,
    SocialPlatformUpdateModel,
    create_social_platform,
    get_one_social_platform,
    get_all_social_platforms,
    update_social_platform,
    remove_social_platform,
)
from core.response_helper import send_response

router = APIRouter()


@router.get("")
def get_social_platforms(db: Session = Depends(database.get_db)):
    platforms = get_all_social_platforms(db=db)

    return send_response(
        "Plataformas sociales obtenidas exitosamente",
        [platform.to_dict() for platform in platforms],
        200,
    )


@router.get("/{platform_id}")
def get_social_platform(platform_id: str = Depends(validate_uuid), db: Session = Depends(database.get_db)):
    platform = get_one_social_platform(db=db, platform_id=platform_id)
    if not platform:
        return send_response("Plataforma social no encontrada", status_code=404)
    return send_response(
        "Plataforma social obtenida exitosamente", platform.to_dict(), 200
    )


@router.post("")
def post_social_platform(
    platform: SocialPlatformCreateModel, db: Session = Depends(database.get_db)
):
    created_platform = create_social_platform(db=db, platform=platform)
    return send_response(
        "Plataforma social creada exitosamente", created_platform.to_dict(), 201
    )


@router.patch("/{platform_id}")
def patch_social_platform(
    platform_id: str,
    platform_update: SocialPlatformUpdateModel,
    db: Session = Depends(database.get_db),
):
    try:
        updated_platform = update_social_platform(
            db=db, platform_id=platform_id, platform_update=platform_update
        )
        return send_response(
            "Plataforma social actualizada exitosamente",
            updated_platform.to_dict(),
            200,
        )

    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/{platform_id}")
def delete_social_platform(platform_id: str, db: Session = Depends(database.get_db)):
    success = remove_social_platform(db=db, platform_id=platform_id)
    if not success:
        return send_response("Plataforma social no encontrada", status_code=404)
    return send_response("Plataforma social eliminada exitosamente", status_code=200)
