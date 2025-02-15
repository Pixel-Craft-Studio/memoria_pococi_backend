from sqlalchemy import Column
from sqlalchemy.dialects.mssql import NVARCHAR, DATETIMEOFFSET, UNIQUEIDENTIFIER
from datetime import datetime, timezone
from uuid import uuid4
from db_models.db_base import Base

# Modelo para la tabla tbl_social_platform
class SocialPlatform(Base):
    __tablename__ = "tbl_social_platform"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)  # Usamos UUID
    name = Column(NVARCHAR(60), nullable=False, unique=True)
    icon_url = Column(NVARCHAR(1024))
    created_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DATETIMEOFFSET,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": str(self.id),  # Convertimos el UUID a string
            "name": self.name,
            "icon_url": self.icon_url,
        }