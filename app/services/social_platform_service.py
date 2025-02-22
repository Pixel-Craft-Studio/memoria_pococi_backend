from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from services.images_service import upload_image, delete_image
from db.db_models.db_social_platform import SocialPlatform
from api_models.social_platform import (
    SocialPlatformCreateModel,
    SocialPlatformUpdateModel,
)


# Crear una nueva plataforma social
def create_social_platform(db: Session, platform: SocialPlatformCreateModel, icon):
    custom_id = uuid4()

    db_platform = SocialPlatform(
        id=custom_id,
        name=platform.name,
    )

    try:
        """Crear una plataforma social con su imagen"""
        prefix = "social-platforms"
        folder = str(db_platform.id)
        file_data = upload_image(icon, prefix, folder)
        icon_url = f"/{prefix}/{folder}/{file_data['filename']}"
        db_platform.icon_url = icon_url

        db.add(db_platform)
        db.commit()
        db.refresh(db_platform)
        return db_platform

    except IntegrityError:
        db.rollback()
        raise ValueError(
            f"Ya existe una plataforma social con el nombre '{platform.name}'."
        )
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


# Obtener una plataforma social por ID
def get_one_social_platform(db: Session, platform_id: UUID):
    return db.query(SocialPlatform).filter(SocialPlatform.id == platform_id).first()


# Obtener todas las plataformas sociales
def get_all_social_platforms(db: Session):
    return db.query(SocialPlatform).all()


# Actualizar una plataforma social
def update_social_platform(
    db: Session,
    platform_id: UUID,
    platform_update: SocialPlatformUpdateModel,
    icon=None,
):
    # Obtener la plataforma social por ID
    db_platform = (
        db.query(SocialPlatform).filter(SocialPlatform.id == platform_id).first()
    )

    if not db_platform:
        raise ValueError(f"No se encontró la plataforma social con ID: {platform_id}")

    # Verificar si el nuevo nombre ya existe antes de actualizar
    if platform_update.name:
        existing_platform = (
            db.query(SocialPlatform)
            .filter(SocialPlatform.name == platform_update.name)
            .first()
        )

        if existing_platform and str(existing_platform.id) != platform_id:
            raise ValueError(
                f"Ya existe otra plataforma social con el nombre '{platform_update.name}'."
            )
        db_platform.name = platform_update.name

    # Si se ha pasado un nuevo icono, se debe subir la imagen y actualizar la URL
    if icon:
        try:
            prefix = "social-platforms"
            folder = str(db_platform.id)
            print("Deleting images")
            delete_image(prefix=prefix, folder=folder)
            file_data = upload_image(icon, prefix, folder)
            icon_url = f"/{prefix}/{folder}/{file_data['filename']}"
            db_platform.icon_url = icon_url
        except Exception as e:
            raise Exception(f"Error al subir el icono: {str(e)}")

    try:
        db.commit()
        db.refresh(db_platform)
        return db_platform
    except IntegrityError:
        db.rollback()
        raise ValueError(
            f"Ya existe una plataforma social con el nombre '{platform_update.name}'."
        )
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


# Eliminar una plataforma social
def remove_social_platform(db: Session, platform_id: UUID):
    db_platform = (
        db.query(SocialPlatform).filter(SocialPlatform.id == platform_id).first()
    )

    if db_platform:
        db.delete(db_platform)

        prefix = "social-platforms"
        folder = str(db_platform.id)
        delete_image(prefix=prefix, folder=folder)

        db.commit()
        return True
    return False
