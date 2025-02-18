from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, TIMESTAMP
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER, DATETIMEOFFSET
from datetime import datetime, timezone
from uuid import uuid4
from db.base import Base


class SocialPlatform(Base):
    __tablename__ = "tbl_social_platform"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"),
        primary_key=True,
        default=uuid4,
    )
    name = Column(String(60), nullable=False, unique=True)
    icon_url = Column(String(1024))
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
            "icon_url": self.icon_url,
        }
