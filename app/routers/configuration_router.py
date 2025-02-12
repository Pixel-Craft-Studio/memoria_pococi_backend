from core.response_helper import send_response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from services.configuration_service import (
    ConfigurationModel,
    create_or_update_configuration,
    get_configuration,
    get_all_configurations,
    delete_configuration,
)

router = APIRouter()


@router.get("")
def get_all_configs(db: Session = Depends(database.get_db)):
    configurations = get_all_configurations(db=db)
    return send_response(
        "Configuraciones obtenidas exitosamente",
        [configuration.to_dict() for configuration in configurations],
        200,
    )


@router.get("/{key}")
def get_config(key: str, db: Session = Depends(database.get_db)):
    key = key
    configuration = get_configuration(db=db, key=key)
    if not configuration:
        return send_response("Configuración no encontrada", status_code=404)
    return send_response(
        "Configuraciones obtenida exitosamente", configuration.to_dict(), 200
    )


@router.post("")
def create_or_update_config(
    config: ConfigurationModel, db: Session = Depends(database.get_db)
):
    configuration = create_or_update_configuration(db=db, config=config)
    return send_response(
        "Configuración gestionada exitosamente", configuration.to_dict(), 200
    )


@router.delete("/{key}")
def delete_config(key: str, db: Session = Depends(database.get_db)):
    key = key

    if not delete_configuration(db=db, key=key):
        return send_response("Configuración no encontrada", status_code=404)

    return send_response("Configuración eliminada exitosamente", status_code=200)
