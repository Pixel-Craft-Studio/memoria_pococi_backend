import json
from sqlalchemy import (
    create_engine,
    Column,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR, DATETIMEOFFSET, VARCHAR
from datetime import datetime
from core.config import settings
from datetime import datetime, timezone

from db_models.db_base import Base

class Configuration(Base):
    __tablename__ = "tbl_configuration"

    key = Column(VARCHAR(64), primary_key=True)
    content = Column(NVARCHAR, nullable=False)
    created_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DATETIMEOFFSET,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "key": self.key,
            "content": json.loads(self.content) if self.content else None,
        }

