from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID  # Importamos UUID para manejarlo correctamente


# Base model para TeamMember
class TeamMemberBaseModel(BaseModel):
    name: str
    photo_url: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None


# Modelo para la creación de redes sociales asociadas a un TeamMember
class SocialMediaCreate(BaseModel):
    platform_id: UUID  # Cambiado a UUID
    url: str


# Modelo para crear un nuevo TeamMember
class TeamMemberCreateModel(TeamMemberBaseModel):
    social_media: Optional[List[SocialMediaCreate]] = None


# Modelo para actualizar un TeamMember
class TeamMemberUpdateModel(TeamMemberBaseModel):
    social_media: Optional[List[SocialMediaCreate]] = None


# Modelo de respuesta para TeamMember
class TeamMemberResponseModel(TeamMemberBaseModel):
    id: UUID  # Cambiado a UUID

    class Config:
        orm_mode = True
