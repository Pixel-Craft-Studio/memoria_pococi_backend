import json

from sqlalchemy.orm import Session
from db.db_models.db_configuration_models import Configuration
from api_models.configuration import ConfigurationModel
from services.images_service import upload_image, delete_image

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

def update_about_configuration(db: Session, config: ConfigurationModel, old_key: str, image=None):
    old_key_lower = old_key.lower()

    db_config = db.query(Configuration).filter(Configuration.key == old_key_lower).first()

    if not db_config:
        raise ValueError(f"Configuración no encontrada '{old_key}'.")
    
    content = json.loads(db_config.content)

    if image:
        try:
            prefix = "configuration"
            folder = "about-us"
            delete_image(prefix=prefix, folder=folder)
            file_data = upload_image(image, prefix, folder)
            image_url = f"/{prefix}/{folder}/{file_data.get('filename')}"
            content["image_url"] = image_url
        except Exception as e:
            raise Exception(f"Error al subir la imagen: {str(e)}")

    if "description" in config.content:
        content["description"] = config.content.get("description")

    db_config.content = json.dumps(content)

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
