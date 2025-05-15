import json
from core.login_helper import get_current_user
from fastapi import APIRouter, Depends, Form, File, UploadFile
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
from db import database
from services.timeline_history_service import (
    create_timeline_history,
    get_one_timeline_history,
    get_all_timeline_histories,
    update_timeline_history,
    remove_timeline_history,
)
from api_models.timeline_history import HistoryStatus
from api_models.timeline_history import (
    TimelineHistoryCreateModel,
    TimelineHistoryUpdateModel,
)

from core.response_helper import send_response

router = APIRouter()


@router.get("")
def get_timeline_histories(db: Session = Depends(database.get_db)):
    """Obtiene todos los registros de TimelineHistory."""
    timeline_histories = get_all_timeline_histories(db=db)
    return send_response(
        "Historias de la línea de tiempo obtenidos exitosamente",
        [timeline_history.to_dict() for timeline_history in timeline_histories],
        200,
    )


@router.get("/{id}")
def get_timeline_history(id: str, db: Session = Depends(database.get_db)):
    """Obtiene un historia de línea de tiempo específico por su ID."""
    timeline_history = get_one_timeline_history(db=db, history_id=id)
    if not timeline_history:
        return send_response(
            "Historia de la línea de tiempo no encontrado", status_code=404
        )
    return send_response(
        "Historia de la línea de tiempo obtenido exitosamente",
        timeline_history.to_dict(),
        200,
    )


@router.post("")
def post_timeline_history(
    title: str = Form(...),
    description: str = Form(...),
    timeline_id: str = Form(...),
    event_date: Optional[datetime] = Form(None),
    image: Optional[UploadFile] = File(...),
    categories: Optional[List[str]] = Form([]),
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    """Crea un nuevo historia de la línea de tiempo."""
    timeline_history = TimelineHistoryCreateModel(
        title=title,
        description=description,
        timeline_id=timeline_id,
        event_date=event_date.strftime("%Y-%m-%d %H:%M:%S"),
        categories=categories,
    )
    print(categories)
    try:
        created_timeline_history = create_timeline_history(
            db=db, timeline_history=timeline_history, image=image
        )
        return send_response(
            "Historia de la línea de tiempo creado exitosamente",
            created_timeline_history.to_dict(),
            201,
        )
    except Exception as e:
        return send_response(f"Error al crear historia: {e}", status_code=400)


@router.patch("/{id}")
def patch_timeline_history(
    id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    event_date: Optional[datetime] = Form(None),
    image: Optional[UploadFile] = File(None),
    categories: Optional[List[str]] = Form(None),
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):

    if event_date:
        event_date=event_date.strftime("%Y-%m-%d %H:%M:%S"),

    timeline_history_update = TimelineHistoryUpdateModel(
        title=title,
        description=description,
        status=status,
        categories=categories,
    )

    try:
        updated_timeline_history = update_timeline_history(
            db=db, history_id=id, timeline_history_update=timeline_history_update, image=image
        )
        return send_response(
            "Historia de la línea de tiempo actualizado exitosamente",
            updated_timeline_history.to_dict(),
            200,
        )
    except Exception as e:
        return send_response(f"Error al actualizar historia: {e}", status_code=400)


@router.delete("/{id}")
def delete_timeline_history(
    id: str,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    """Elimina un historia de la línea de tiempo por su ID."""
    success = remove_timeline_history(db=db, id=id)
    if not success:
        return send_response(
            "Historia de la línea de tiempo no encontrado", status_code=404
        )
    return send_response(
        "Historia de la línea de tiempo eliminado exitosamente", status_code=200
    )
