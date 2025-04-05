from uuid import uuid4
from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import DATETIMEOFFSET, UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import (
    TIMESTAMP as PostgresTIMESTAMP,
    UUID as PostgresUUID,
)
from datetime import datetime, timezone
from db.base import Base


class TimelineYear(Base):
    __tablename__ = "tbl_timeline_year"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"),
        primary_key=True,
        default=uuid4,
    )

    year = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    created_at = Column(
        DATETIMEOFFSET().with_variant(PostgresTIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DATETIMEOFFSET().with_variant(PostgresTIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, default=True)

    histories = relationship("TimelineHistory", back_populates="timeline")

    def to_dict(self):
        return {
            "id": str(self.id),
            "year": self.year,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "histories": [history.to_dict() for history in self.histories],
        }
