from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.dialects.mssql import VARCHAR, DATETIMEOFFSET, UNIQUEIDENTIFIER
from datetime import datetime, timezone
from db_models.db_base import Base
from uuid import uuid4


class Profile(Base):
    __tablename__ = "tbl_profile"

    id = Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(VARCHAR(60), nullable=False)  # Limite de 60 caracteres
    last_name = Column(VARCHAR(60), nullable=False)  # Limite de 60 caracteres
    email = Column(
        VARCHAR(255), nullable=False, unique=True
    )  # Limite de 255 caracteres
    password_hash = Column(VARCHAR(255), nullable=False)  # Limite de 255 caracteres
    created_at = Column(
        DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc)
    )  # Fecha de creación con zona horaria
    updated_at = Column(
        DATETIMEOFFSET,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )  # Fecha de actualización con zona horaria
    is_active = Column(Boolean, default=True)  # Valor por defecto 1 (activo)

    def to_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }

    def to_response_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
        }
