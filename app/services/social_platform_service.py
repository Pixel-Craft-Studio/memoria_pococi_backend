import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db_models.db_team_member_models import SocialPlatform
from api_models.social_platform import SocialPlatformCreateModel, SocialPlatformUpdateModel

# Crear una nueva plataforma social
def create_social_platform(db: Session, platform: SocialPlatformCreateModel):
    platform_id = str(uuid.uuid4())

    db_platform = SocialPlatform(
        id=platform_id,
        name=platform.name,
        icon_url=platform.icon_url,
    )

    try:
        db.add(db_platform)
        db.commit()
        db.refresh(db_platform)
        return db_platform

    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe una plataforma social con el nombre '{platform.name}'.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


# Obtener una plataforma social por ID
def get_one_social_platform(db: Session, platform_id: str):
    return db.query(SocialPlatform).filter(SocialPlatform.id == platform_id).first()


# Obtener todas las plataformas sociales
def get_all_social_platforms(db: Session):
    return db.query(SocialPlatform).all()


# Actualizar una plataforma social
def update_social_platform(db: Session, platform_id: str, platform_update: SocialPlatformUpdateModel):
    db_platform = db.query(SocialPlatform).filter(SocialPlatform.id == platform_id).first()

    if not db_platform:
        raise ValueError(f"No se encontró la plataforma social con ID: {platform_id}")

    # Verificar si el nuevo nombre ya existe antes de actualizar
    if platform_update.name:
        existing_platform = db.query(SocialPlatform).filter(SocialPlatform.name == platform_update.name).first()
        if existing_platform and existing_platform.id != platform_id:
            raise ValueError(f"Ya existe otra plataforma social con el nombre '{platform_update.name}'.")

        db_platform.name = platform_update.name

    if platform_update.icon_url:
        db_platform.icon_url = platform_update.icon_url

    try:
        db.commit()
        db.refresh(db_platform)
        return db_platform
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe una plataforma social con el nombre '{platform_update.name}'.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


# Eliminar una plataforma social
def remove_social_platform(db: Session, platform_id: str):
    db_platform = db.query(SocialPlatform).filter(SocialPlatform.id == platform_id).first()

    if db_platform:
        db.delete(db_platform)
        db.commit()
        return True
    return False
