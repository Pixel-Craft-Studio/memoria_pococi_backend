import json

from sqlalchemy.orm import Session
from db.db_models.db_configuration_models import Configuration
from api_models.configuration import ConfigurationModel


def create_configuration(db: Session, config: ConfigurationModel):
    key_lower = config.key.lower()

    existing_key = (
        db.query(Configuration).filter(Configuration.key == config.key).first()
    )

    if existing_key:
        raise ValueError(f"Ya existe una clave con el id '{config.key}'.")

    db_configuration = Configuration(key=key_lower, content=json.dumps(config.content))
    db.add(db_configuration)
    db.commit()
    db.refresh(db_configuration)
    return db_configuration


def update_configuration(db: Session, config: ConfigurationModel, old_key: str):
    old_key_lower = old_key.lower()

    db_config = db.query(Configuration).filter(Configuration.key == old_key_lower).first()

    if not db_config:
        raise ValueError(f"Configuración no encontrada '{old_key}'.")

    update_data = config.dict(exclude_unset=True)

    # Actualizar la clave si es necesario
    if "key" in update_data:
        new_key_lower = update_data["key"].lower()

        if new_key_lower != old_key_lower:
            existing_key = db.query(Configuration).filter(Configuration.key == new_key_lower).first()
            if existing_key:
                raise ValueError(f"Ya existe una configuración con el nombre '{update_data['key']}'.")

            db_config.key = new_key_lower

    # Actualizar el contenido si es necesario
    if "content" in update_data:
        db_config.content = json.dumps(update_data["content"])

    db.commit()
    db.refresh(db_config)
    return db_config

def get_configuration(db: Session, key: str):
    key_lower = key.lower()
    return db.query(Configuration).filter(Configuration.key == key_lower).first()


def get_all_configurations(db: Session):
    return db.query(Configuration).all()


def delete_configuration(db: Session, key: str):
    key_lower = key.lower()
    config = db.query(Configuration).filter(Configuration.key == key_lower).first()
    if config:
        db.delete(config)
        db.commit()
        return True
    return False
