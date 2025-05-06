from typing import Optional
from core.login_helper import get_current_user
from db.db_models.db_configuration_models import Configuration
from services.images_service import upload_image, delete_image
from core.response_helper import send_response
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from db import database
from services.configuration_service import (
    ConfigurationModel,
    create_configuration,
    update_about_configuration,
    update_configuration,
    get_configuration,
    get_all_configurations,
    delete_configuration,
)

router = APIRouter()

# Specific configuration endpoints.


@router.get("/about-us")
def get_about_config(db: Session = Depends(database.get_db)):
    configuration = get_configuration(db, "about-us")
    if not configuration:
        config = Configuration(
            key="about-us", content={"description": "Description", "image_url": "/none"}
        )
        configuration = create_configuration(db, config)

    return send_response(
        "Configuración obtenida exitosamente", configuration.to_dict(), 200
    )


@router.patch("/about-us")
def update_about_config(
    description: str = Form(...),
    image: Optional[UploadFile] = File(default=None),
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    configuration = ConfigurationModel(
        key="about-us",
        content={
            "description": description,
        },
    )

    configuration = update_about_configuration(db, configuration, "about-us", image)

    return send_response(
        "Configuración actualizada exitosamente", configuration.to_dict(), 200
    )


# General configuration endpoints
@router.get("")
def get_all_configs(
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    configurations = get_all_configurations(db=db)
    return send_response(
        "Configuraciones obtenidas exitosamente",
        [configuration.to_dict() for configuration in configurations],
        200,
    )


@router.get("/{key}")
def get_config(
    key: str,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    configuration = get_configuration(db, key)
    if not configuration:
        return send_response("Configuración no encontrada", status_code=404)
    return send_response(
        "Configuración obtenida exitosamente", configuration.to_dict(), 200
    )


@router.post("")
def create_config(
    config: ConfigurationModel,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        configuration = create_configuration(db, config)

        return send_response(
            "Configuración creada exitosamente", configuration.to_dict(), 200
        )

    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.patch("/{key}")
def update_config(
    key: str,
    config: ConfigurationModel,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    configuration = update_configuration(db, config, key)

    return send_response(
        "Configuración actualizada exitosamente", configuration.to_dict(), 200
    )


@router.delete("/{key}")
def delete_config(
    key: str,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    if not delete_configuration(db, key):
        return send_response("Configuración no encontrada", status_code=404)

    return send_response("Configuración eliminada exitosamente", status_code=200)
