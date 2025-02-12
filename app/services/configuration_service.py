import json

from sqlalchemy.orm import Session
from db_models.db_configuration_models import Configuration
from api_models.configuration import ConfigurationModel

def create_or_update_configuration(db: Session, config: ConfigurationModel):
    key_lower = config.key.lower()

    db_config = db.query(Configuration).filter(Configuration.key == key_lower).first()

    if db_config:
        # Actualizar solo los campos proporcionados en la solicitud
        update_data = config.dict(exclude_unset=True)

        if "content" in update_data:
            db_config.content = json.dumps(update_data["content"])

        db.commit()
        db.refresh(db_config)
        return db_config
    else:
        # Guardar la clave en minúsculas
        db_configuration = Configuration(
            key=key_lower, content=json.dumps(config.content)
        )
        db.add(db_configuration)
        db.commit()
        db.refresh(db_configuration)
        return db_configuration


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
