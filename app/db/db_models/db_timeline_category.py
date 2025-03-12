from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, TIMESTAMP
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER, DATETIMEOFFSET
from datetime import datetime, timezone
from db.base import Base


class TimelineCategory(Base):
    __tablename__ = "tbl_timeline_category"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"),
        primary_key=True,
        default=uuid4,
    )
    name = Column(String(64), nullable=False, unique=True)

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
        }
