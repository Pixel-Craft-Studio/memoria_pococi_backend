import json
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mssql import NVARCHAR, DATETIMEOFFSET
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP
from datetime import datetime, timezone
from db.base import Base


class Configuration(Base):
    __tablename__ = "tbl_configuration"

    key = Column(NVARCHAR(64).with_variant(String(64), "postgresql"), primary_key=True)
    content = Column(NVARCHAR(None).with_variant(TEXT, "postgresql"), nullable=False)

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
            "key": self.key,
            "content": json.loads(self.content) if self.content else None,
        }
