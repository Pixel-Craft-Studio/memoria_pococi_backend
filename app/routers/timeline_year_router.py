import json
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from db import database
from services.timeline_year_service import (
    TimelineYearCreateModel,
    TimelineYearUpdateModel,
    create_timeline_year,
    get_one_timeline_year,
    get_one_timeline_year_by_year,
    get_all_timeline_years,
    update_timeline_year,
    remove_timeline_year,
)
from services.timeline_history_service import (
    remove_timeline_history_by_year_id
)
from core.response_helper import send_response

router = APIRouter()


@router.get("")
def get_timeline_years(db: Session = Depends(database.get_db)):
    timeline_years = get_all_timeline_years(db=db)
    return send_response(
        "Años de la línea de tiempo obtenidos exitosamente",
        [timeline_year.to_dict() for timeline_year in timeline_years],
        200,
    )


@router.get("/year/{year}")
def get_timeline_year_by_year(year: str, db: Session = Depends(database.get_db)):
    timeline_year = get_one_timeline_year_by_year(db=db, year=year)
    if not timeline_year:
        return send_response("Año de la línea de tiempo no encontrado", status_code=404)
    return send_response(
        "Año de la línea de tiempo obtenido exitosamente",
        timeline_year.to_dict(),
        200,
    )

@router.get("/{id}")
def get_timeline_year(id: str, db: Session = Depends(database.get_db)):
    timeline_year = get_one_timeline_year(db=db, id=id)
    if not timeline_year:
        return send_response("Año de la línea de tiempo no encontrado", status_code=404)
    return send_response(
        "Año de la línea de tiempo obtenido exitosamente",
        timeline_year.to_dict(),
        200,
    )


@router.post("")
def post_timeline_year(
    year: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    image: Optional[UploadFile] = File(...),
    
    db: Session = Depends(database.get_db),
):
    timeline_year = TimelineYearCreateModel(
        year=year, title=title, description=description
    )

    try:
        created_timeline_year = create_timeline_year(
            db=db, timeline_year=timeline_year, image=image
        )
        return send_response(
            "Año de la línea de tiempo creado exitosamente",
            created_timeline_year.to_dict(),
            201,
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.patch("/{id}")
def patch_timeline_year(
    id:str,
    year: Optional[int] = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    is_active: Optional[bool] = Form(None),
    db: Session = Depends(database.get_db),
):
    timeline_year_update = TimelineYearUpdateModel(
        year=year, title=title, description=description, is_active=is_active
    )

    try:
        updated_timeline_year = update_timeline_year(
            db=db, id=id, timeline_year_update=timeline_year_update, image=image
        )
        return send_response(
            "Año de la línea de tiempo actualizado exitosamente",
            updated_timeline_year.to_dict(),
            200,
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/{id}")
def delete_timeline_year(id: str, db: Session = Depends(database.get_db)):
    
    histories_success = remove_timeline_history_by_year_id(db=db, year_id=id)

    success = remove_timeline_year(db=db, id=id)
    if not success:
        return send_response("Año de la línea de tiempo no encontrado", status_code=404)
    return send_response("Año de la línea de tiempo eliminado exitosamente", status_code=200)
