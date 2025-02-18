from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mssql import VARCHAR, DATETIMEOFFSET, UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, TIMESTAMP
from datetime import datetime, timezone
from db.base import Base
from uuid import uuid4


class Profile(Base):
    __tablename__ = "tbl_profile"

    id = Column(
        UNIQUEIDENTIFIER(as_uuid=True).with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ),
        primary_key=True,
        default=uuid4,
    )
    first_name = Column(
        VARCHAR(60).with_variant(String(60), "postgresql"), nullable=False
    )
    last_name = Column(
        VARCHAR(60).with_variant(String(60), "postgresql"), nullable=False
    )
    email = Column(
        VARCHAR(255).with_variant(String(255), "postgresql"),
        nullable=False,
        unique=True,
    )
    password_hash = Column(
        VARCHAR(255).with_variant(String(255), "postgresql"), nullable=False
    )
    created_at = Column(
        DATETIMEOFFSET().with_variant(TIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DATETIMEOFFSET().with_variant(TIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, default=True)

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
