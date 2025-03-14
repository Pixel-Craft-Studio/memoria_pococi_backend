from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import VARCHAR, DATETIMEOFFSET, UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, TIMESTAMP
from datetime import datetime, timezone
from db.base import Base
from uuid import uuid4

class RecoveryPassword(Base):
    __tablename__ = "tbl_recovery_password"

    id = Column(
        UNIQUEIDENTIFIER(as_uuid=True).with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ),
        primary_key=True,
        default=uuid4,
    )
    profile_id = Column(
        UNIQUEIDENTIFIER(as_uuid=True).with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ),
        ForeignKey("tbl_profile.id", ondelete="CASCADE"),
        nullable=False,
    )
    password = Column(
        VARCHAR(255).with_variant(String(255), "postgresql"), nullable=False
    )
    expiration = Column(
        DateTime(timezone=True), nullable=False
    )

    profile = relationship("Profile", backref="recovery_password")

    created_at = Column(
        DATETIMEOFFSET().with_variant(TIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DATETIMEOFFSET().with_variant(TIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "profile_id": str(self.profile_id),
            "password": self.password,
            "expiration": self.expiration.isoformat() if self.expiration else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_response_dict(self):
        return {
            "id": str(self.id),
            "profile_id": str(self.profile_id),
            "password": self.password,
            "expiration": self.expiration.isoformat() if self.expiration else None,
        }
