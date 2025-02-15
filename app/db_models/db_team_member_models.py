from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR, DATETIMEOFFSET, UNIQUEIDENTIFIER
from datetime import datetime, timezone
from uuid import uuid4
from db_models.db_base import Base


# Modelo para la tabla tbl_team_member
class TeamMember(Base):
    __tablename__ = "tbl_team_member"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)  # Usamos UUID
    name = Column(NVARCHAR(60), nullable=False)
    photo_url = Column(NVARCHAR(2048))
    description = Column(NVARCHAR(500))
    role = Column(NVARCHAR(100))
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
            "id": str(self.id),  # Convertimos el UUID a string
            "name": self.name,
            "photo_url": self.photo_url,
            "description": self.description,
            "role": self.role,
            "social_media": [
                sm.to_dict() for sm in self.social_media
            ],  # Agregando los datos de las redes sociales
        }


# Modelo para la tabla tbl_social_media
class SocialMedia(Base):
    __tablename__ = "tbl_social_media"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)  # Usamos UUID
    team_member_id = Column(
        UNIQUEIDENTIFIER, ForeignKey("tbl_team_member.id", ondelete="CASCADE")
    )
    url = Column(NVARCHAR(2048), nullable=False)
    platform_id = Column(
        UNIQUEIDENTIFIER, ForeignKey("tbl_social_platform.id", ondelete="CASCADE")
    )
    updated_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DATETIMEOFFSET, default=lambda: datetime.now(timezone.utc))

    # Relación con TeamMember
    team_member = relationship("TeamMember", back_populates="social_media")

    # Relación con SocialPlatform
    platform = relationship("SocialPlatform", backref="social_media")

    def to_dict(self):
        return {
            "id": str(self.id),  # Convertimos el UUID a string
            "platform_id": str(self.platform_id),  # Convertimos el UUID a string
            "platform": self.platform.name,
            "icon_url": self.platform.icon_url,
            "url": self.url,
        }
