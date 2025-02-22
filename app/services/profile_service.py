from core.login_helper import hash_password
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.db_models.db_profile import Profile
from api_models.profile import (
    ProfileCreateModel,
    ProfileUpdateModel,
)


def create_profile(db: Session, profile: ProfileCreateModel):
    hashed_password = hash_password(profile.password)

    db_profile = Profile(
        first_name=profile.first_name,
        last_name=profile.last_name,
        email=profile.email,
        password_hash=hashed_password,
    )

    try:
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig).lower()

        if "unique constraint" in error_msg or "duplicate key" in error_msg:
            raise ValueError(f"Ya existe un perfil con el correo '{profile.email}'.")
        elif "not null" in error_msg:
            raise ValueError("Falta un valor obligatorio.")
        else:
            raise ValueError(f"Error de integridad desconocido'{str(e)}'")

    except Exception as e:
        db.rollback()

        raise RuntimeError(f"Error inesperado '{str(e)}'")


# Obtener un Perfil por ID
def get_one_profile(db: Session, profile_id: UUID):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    return profile if profile else None


def get_profile_by_email(db: Session, email: str):
    profile = (
        db.query(Profile).filter(Profile.email == email, Profile.is_active).first()
    )
    return profile


# Obtener Todos los Perfiles
def get_all_profiles(db: Session):
    return db.query(Profile).all()


# Actualizar un Perfil
def update_profile(db: Session, profile_id: UUID, profile_update: ProfileUpdateModel):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not db_profile:
        raise ValueError(f"No se encontró el perfil con ID: {profile_id}")

    # Verificar si el correo ya está en uso por otro perfil
    if profile_update.email:
        existing_profile = (
            db.query(Profile).filter(Profile.email == profile_update.email).first()
        )
        if existing_profile and existing_profile.id != profile_id:
            raise ValueError(
                f"Ya existe un perfil con el correo '{profile_update.email}'."
            )

        db_profile.email = profile_update.email

    if profile_update.first_name:
        db_profile.first_name = profile_update.first_name

    if profile_update.last_name:
        db_profile.last_name = profile_update.last_name

    if profile_update.is_active is not None:
        db_profile.is_active = profile_update.is_active

    try:
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe un perfil con el correo '{profile_update.email}'.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


# Eliminar un Perfil
def remove_profile(db: Session, profile_id: UUID):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if db_profile:
        db.delete(db_profile)
        db.commit()
        return True
    return False
