from typing import Optional

from core.login_helper import get_current_user
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from db import database
from services.timeline_section_service import (
    TimelineSectionCreateModel,
    TimelineSectionUpdateModel,
    create_timeline_section,
    get_one_timeline_section,
    get_all_timeline_sections,
    get_sections_by_history_id,
    update_timeline_section,
    remove_timeline_section,
)
from core.response_helper import send_response

router = APIRouter()


@router.get("")
def get_timeline_sections(db: Session = Depends(database.get_db)):
    timeline_sections = get_all_timeline_sections(db=db)
    return send_response(
        "Secciones de la línea de tiempo obtenidas exitosamente",
        [section.to_dict() for section in timeline_sections],
        200,
    )


@router.get("/history/{history_id}")
def get_timeline_sections_by_history(
    history_id: str, db: Session = Depends(database.get_db)
):
    sections = get_sections_by_history_id(db=db, history_id=history_id)
    return send_response(
        "Secciones de la línea de tiempo obtenidas exitosamente",
        [section.to_dict() for section in sections],
        200,
    )


@router.get("/{id}")
def get_timeline_section(id: str, db: Session = Depends(database.get_db)):
    timeline_section = get_one_timeline_section(db=db, id=id)
    if not timeline_section:
        return send_response(
            "Sección de la línea de tiempo no encontrada", status_code=404
        )
    return send_response(
        "Sección de la línea de tiempo obtenida exitosamente",
        timeline_section.to_dict(),
        200,
    )


@router.post("")
def post_timeline_section(
    history_id: str = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    template: Optional[str] = Form(None),
    isInverted: Optional[bool] = Form(False),
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    timeline_section = TimelineSectionCreateModel(
        history_id=history_id,
        title=title,
        description=description,
        template=template,
        isInverted=isInverted,
    )

    try:
        created_timeline_section = create_timeline_section(
            db=db, timeline_section=timeline_section, image=image
        )
        return send_response(
            "Sección de la línea de tiempo creada exitosamente",
            created_timeline_section.to_dict(),
            201,
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.patch("/{id}")
def patch_timeline_section(
    id: str,
    history_id: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    template: Optional[str] = Form(None),
    isInverted: Optional[bool] = Form(None),
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    timeline_section_update = TimelineSectionUpdateModel(
        history_id=history_id,
        title=title,
        description=description,
        template=template,
        isInverted=isInverted,
    )

    try:
        updated_timeline_section = update_timeline_section(
            db=db, id=id, timeline_section_update=timeline_section_update, image=image
        )
        return send_response(
            "Sección de la línea de tiempo actualizada exitosamente",
            updated_timeline_section.to_dict(),
            200,
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/{id}")
def delete_timeline_section(
    id: str,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    success = remove_timeline_section(db=db, id=id)
    if not success:
        return send_response(
            "Sección de la línea de tiempo no encontrada", status_code=404
        )
    return send_response(
        "Sección de la línea de tiempo eliminada exitosamente", status_code=200
    )
