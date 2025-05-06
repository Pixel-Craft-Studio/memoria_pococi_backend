from typing import Optional
from core.login_helper import get_current_user
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from db import database
from services.timeline_category_service import (
    create_timeline_category,
    get_one_timeline_category,
    get_all_timeline_categories,
    update_timeline_category,
    remove_timeline_category,
)
from core.response_helper import send_response
from api_models.timeline_category import (
    TimelineCategoryCreateModel,
    TimelineCategoryUpdateModel,
)
from core.validate_helper import validate_uuid

router = APIRouter()

@router.get("")
def get_timeline_categories(db: Session = Depends(database.get_db)):
    categories = get_all_timeline_categories(db=db)
    return send_response(
        "Categorías de línea de tiempo obtenidas exitosamente",
        [category.to_dict() for category in categories],
        200,
    )

@router.get("/{category_id}")
def get_timeline_category(
    category_id: str = Depends(validate_uuid), db: Session = Depends(database.get_db)
):
    category = get_one_timeline_category(db=db, category_id=category_id)

    if not category:
        return send_response("Categoría no encontrada", status_code=404)
    return send_response(
        "Categoría de línea de tiempo obtenida exitosamente", category.to_dict(), 200
    )

@router.post("")
async def post_timeline_category(
    category: TimelineCategoryCreateModel, db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        created_category = create_timeline_category(
            db=db, category=category
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)

    return send_response(
        "Categoría de línea de tiempo creada exitosamente", created_category.to_dict(), 201
    )

@router.patch("/{category_id}")
def patch_timeline_category(
    category_id: str,
    category_update: TimelineCategoryUpdateModel = Body(...),
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        updated_category = update_timeline_category(
            db=db,
            category_id=category_id,
            category_update=category_update,
        )
        return send_response(
            "Categoría de línea de tiempo actualizada exitosamente",
            updated_category.to_dict(),
            200,
        )

    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/{category_id}")
def delete_timeline_category(
    category_id: str, db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    success = remove_timeline_category(db=db, category_id=category_id)
    if not success:
        return send_response("Categoría no encontrada", status_code=404)
    return send_response("Categoría de línea de tiempo eliminada exitosamente", status_code=200)
