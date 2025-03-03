from api_models.contact_us import ContactStatus
from sqlalchemy import Column, String, TIMESTAMP, Enum
from sqlalchemy.dialects.mssql import DATETIMEOFFSET, UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from datetime import datetime, timezone
from db.base import Base
from uuid import uuid4


class ContactUs(Base):
    __tablename__ = "tbl_contact_us"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"),
        primary_key=True,
        default=uuid4,
    )
    name = Column(String(60), nullable=False)
    status = Column(
        Enum(ContactStatus, name="contact_status"),
        nullable=False,
        default=ContactStatus.NEW,
    )
    email = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    subject = Column(String(255), nullable=True)
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
            "name": self.name,
            "status": self.status.value,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
