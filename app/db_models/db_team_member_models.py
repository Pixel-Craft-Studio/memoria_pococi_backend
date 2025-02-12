from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR, DATETIMEOFFSET, VARCHAR
from datetime import datetime
from core.config import settings
from datetime import datetime, timezone

from db_models.db_base import Base

# Modelo para la tabla tbl_team_member
class TeamMember(Base):
    __tablename__ = "tbl_team_member"

    id = Column(VARCHAR(60), primary_key=True)
    name = Column(VARCHAR(60), nullable=False)
    photo_url = Column(VARCHAR(2048))
    description = Column(VARCHAR(500))
    role = Column(VARCHAR(100))
    created_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DATETIMEOFFSET,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relación uno a muchos con SocialMedia
    social_media = relationship("SocialMedia", back_populates="team_member")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo_url": self.photo_url,
            "description": self.description,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "social_media": [
                sm.to_dict() for sm in self.social_media
            ],  # Agregando los datos de las redes sociales
        }


# Modelo para la tabla tbl_social_platform
class SocialPlatform(Base):
    __tablename__ = "tbl_social_platform"

    id = Column(VARCHAR(60), primary_key=True)
    name = Column(VARCHAR(60), nullable=False, unique=True)
    icon_url = Column(VARCHAR(1024))
    created_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DATETIMEOFFSET,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon_url": self.icon_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# Modelo para la tabla tbl_social_media
class SocialMedia(Base):
    __tablename__ = "tbl_social_media"

    id = Column(VARCHAR(60), primary_key=True)
    team_member_id = Column(
        VARCHAR(60), ForeignKey("tbl_team_member.id", ondelete="CASCADE")
    )
    url = Column(VARCHAR(2048), nullable=False)
    platform_id = Column(
        VARCHAR(60), ForeignKey("tbl_social_platform.id", ondelete="CASCADE")
    )
    updated_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))

    # Relación con TeamMember
    team_member = relationship("TeamMember", back_populates="social_media")

    # Relación con SocialPlatform
    platform = relationship("SocialPlatform", backref="social_media")

    def to_dict(self):
        return {
            "id": self.id,
            "team_member_id": self.team_member_id,
            "url": self.url,
            "platform_id": self.platform_id,
            "icon_url": self.platform.icon_url,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
