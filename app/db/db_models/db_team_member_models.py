from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR, DATETIMEOFFSET, UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from datetime import datetime, timezone
from uuid import uuid4
from db.base import Base


# Modelo para la tabla tbl_team_member
class TeamMember(Base):
    __tablename__ = "tbl_team_member"

    id = Column(
        UNIQUEIDENTIFIER().with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ),  # Usamos la variante para Postgres
        primary_key=True,
        default=uuid4,
    )
    name = Column(NVARCHAR(60).with_variant(String(60), "postgresql"))
    photo_url = Column(NVARCHAR(2048).with_variant(String(2048), "postgresql"))
    description = Column(NVARCHAR(500).with_variant(String(500), "postgresql"))
    role = Column(NVARCHAR(100).with_variant(String(100), "postgresql"))
    created_at = Column(
        DATETIMEOFFSET().with_variant(
            TIMESTAMP(timezone=True), "postgresql"
        ),  # Usamos la variante para Postgres
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DATETIMEOFFSET().with_variant(
            TIMESTAMP(timezone=True), "postgresql"
        ),  # Usamos la variante para Postgres
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

    id = Column(
        UNIQUEIDENTIFIER().with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ),  # Usamos la variante para Postgres
        primary_key=True,
        default=uuid4,
    )
    team_member_id = Column(
        UNIQUEIDENTIFIER().with_variant(
            PostgresUUID(as_uuid=True), "postgresql"
        ),  # Usamos la variante para Postgres
        ForeignKey("tbl_team_member.id", ondelete="CASCADE"),
    )
    url = Column(
        NVARCHAR(2048).with_variant(String(2048), "postgresql"), nullable=False
    )
    platform_id = Column(
        UNIQUEIDENTIFIER().with_variant(PostgresUUID(as_uuid=True), "postgresql"),
        ForeignKey("tbl_social_platform.id", ondelete="CASCADE"),
    )
    updated_at = Column(
        DATETIMEOFFSET().with_variant(TIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
    )
    created_at = Column(
        DATETIMEOFFSET().with_variant(TIMESTAMP(timezone=True), "postgresql"),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relación con TeamMember
    team_member = relationship("TeamMember", back_populates="social_media")

    # Relación con SocialPlatform
    platform = relationship("SocialPlatform", backref="social_media")

    def to_dict(self):
        return {
            "id": str(self.id),  # Convertimos el UUID a string
            "platform_id": str(self.platform_id),  # Convertimos el UUID a string
            "platform": self.platform.name,
            "image_url": self.platform.image_url,
            "url": self.url,
        }
