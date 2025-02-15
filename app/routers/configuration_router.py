from core.response_helper import send_response
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from services.configuration_service import (
    ConfigurationModel,
    create_configuration,
    update_configuration,
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
    configuration = get_configuration(db, key)
    if not configuration:
        return send_response("Configuración no encontrada", status_code=404)
    return send_response(
        "Configuración obtenida exitosamente", configuration.to_dict(), 200
    )


@router.post("")
def create_config(config: ConfigurationModel, db: Session = Depends(database.get_db)):
    try:
        configuration = create_configuration(db, config)

        return send_response(
            "Configuración creada exitosamente", configuration.to_dict(), 200
        )

    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.patch("/{key}")
def update_config(
    key: str, config: ConfigurationModel, db: Session = Depends(database.get_db)
):
   
        configuration = update_configuration(db, config, key)

        return send_response(
            "Configuración actualizada exitosamente", configuration.to_dict(), 200
        )

  


@router.delete("/{key}")
def delete_config(key: str, db: Session = Depends(database.get_db)):
    if not delete_configuration(db, key):
        return send_response("Configuración no encontrada", status_code=404)

    return send_response("Configuración eliminada exitosamente", status_code=200)
