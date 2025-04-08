from uuid import uuid4
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import DATETIMEOFFSET, UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import TIMESTAMP as PostgresTIMESTAMP, UUID as PostgresUUID
from datetime import datetime, timezone
from db.base import Base


class TimelineSection(Base):
    __tablename__ = "tbl_timeline_section"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ), 
        primary_key=True,
        default=uuid4,
    )
    history_id = Column(
        UNIQUEIDENTIFIER().with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ),
        ForeignKey("tbl_timeline_history.id", ondelete="NO ACTION"),
        nullable=False,
    )
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    image_url = Column(String(2048), nullable=True)
    template = Column(String(64), nullable=True)
    isInverted = Column(Boolean, default=False)
    created_at = Column(
        DATETIMEOFFSET().with_variant(PostgresTIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DATETIMEOFFSET().with_variant(PostgresTIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    history = relationship("TimelineHistory", back_populates="sections")

    def to_dict(self):
        return {
            "id": str(self.id),
            "history_id": str(self.history_id),
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "template": self.template,
            "isInverted": self.isInverted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }