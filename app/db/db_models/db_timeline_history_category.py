from uuid import uuid4
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

class TimelineHistoryCategory(Base):
    __tablename__ = "tbl_timeline_history_category"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"), 
        primary_key=True,
        default=uuid4,
    )
    timeline_history_id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"),
        ForeignKey("tbl_timeline_history.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"),
        ForeignKey("tbl_timeline_category.id", ondelete="CASCADE"),
        nullable=False,
    )

    history = relationship("TimelineHistory", back_populates="categories")
    category = relationship("TimelineCategory")  # Relación con la categoría

    def to_dict(self):
        return self.category.to_dict()
