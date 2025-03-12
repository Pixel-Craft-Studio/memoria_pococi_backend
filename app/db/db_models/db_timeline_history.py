from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import DATETIMEOFFSET, UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, TIMESTAMP as PostgresTIMESTAMP
from datetime import datetime, timezone
from db.base import Base
from api_models.timeline_history import HistoryStatus


class TimelineHistory(Base):
    __tablename__ = "tbl_timeline_history"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ), 
        primary_key=True,
        default=uuid4,
    )
    image_url = Column(String(2048), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    created_at = Column(
        DATETIMEOFFSET().with_variant(PostgresTIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DATETIMEOFFSET().with_variant(PostgresTIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    status = Column(Enum(HistoryStatus), nullable=False, default=HistoryStatus.POSTED)  
    timeline_id = Column(
        Integer,
        ForeignKey("tbl_timeline_year.year", ondelete="CASCADE"),
        nullable=False,
    )
    event_date = Column(
        DATETIMEOFFSET().with_variant(PostgresTIMESTAMP(timezone=True), "postgresql"),
        nullable=False,
    )

    timeline = relationship("TimelineYear", back_populates="histories")
    categories = relationship("TimelineHistoryCategory", back_populates="history")
    sections = relationship("TimelineSection", back_populates="history")

    def to_dict(self):
        return {
            "id": str(self.id),
            "image_url": self.image_url,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "timeline_id": self.timeline_id,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "categories": [category.to_dict() for category in self.categories]
        }
