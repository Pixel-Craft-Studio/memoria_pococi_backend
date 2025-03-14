import string
import secrets

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from db.db_models.db_recovery_password import RecoveryPassword
from db.db_models.db_profile import Profile
from core.login_helper import hash_password


def post_recovery_password(db: Session, email: str):
    profile = db.query(Profile).filter(Profile.email == email).first()
    if not profile:
        return None 

    plain_password = generate_password()

    hashed_password = hash_password(plain_password)
  
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=15)

    existing_recovery = db.query(RecoveryPassword).filter(
        RecoveryPassword.profile_id == profile.id
    ).first()

    if existing_recovery:
        existing_recovery.password = hashed_password
        existing_recovery.expiration = expiration_time
        existing_recovery.updated_at = datetime.now(timezone.utc)
    else:
        new_recovery = RecoveryPassword(
            profile_id=profile.id,
            password=hashed_password,
            expiration=expiration_time,
        )
        db.add(new_recovery)

    db.commit()

    return plain_password

def reset_password(db: Session, profile_id, password):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise ValueError("Perfil no encontrado")

    hashed_password = hash_password(password)
    profile.password_hash = hashed_password
    
    recovery = db.query(RecoveryPassword).filter(RecoveryPassword.profile_id == profile_id).first()
    db.add(profile)
    db.delete(recovery)
    db.commit()

def get_recovery_by_id(db: Session, uuid):
    recovery = (
        db.query(RecoveryPassword).filter(RecoveryPassword.profile_id == uuid).first()
    )
    return recovery

def delete_recovery_by_id(db: Session, uuid):
    recovery = db.query(RecoveryPassword).filter(RecoveryPassword.profile_id == uuid).first()
    
    db.delete(recovery)
    db.commit()

def generate_password(
    length=16,
    min_digits=2,
    max_specials=3,  # Cambiado de min_specials a max_specials
    min_uppercase=2,
    min_lowercase=2,
    special_characters="!@#$%^&*()_+-=[]{}|;:,.<>?",
):

    min_specials = min(2, max_specials) 
    total_min_requirements = min_digits + min_specials + min_uppercase + min_lowercase
    
    if total_min_requirements > length:
        raise ValueError(
            f"The sum of minimum requirements ({total_min_requirements}) exceeds the requested password length ({length})"
        )

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits

    password_chars = (
        [secrets.choice(digits) for _ in range(min_digits)]
        + [secrets.choice(special_characters) for _ in range(min_specials)]
        + [secrets.choice(uppercase) for _ in range(min_uppercase)]
        + [secrets.choice(lowercase) for _ in range(min_lowercase)]
    )
    
    current_special_count = min_specials
    
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        if current_special_count >= max_specials:
            alphanumeric = lowercase + uppercase + digits
            password_chars.append(secrets.choice(alphanumeric))
        else:
            all_chars = lowercase + uppercase + digits + special_characters
            char = secrets.choice(all_chars)
            password_chars.append(char)
            if char in special_characters:
                current_special_count += 1

    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)