from pydantic import BaseModel
from typing import Optional
from uuid import UUID  # Importamos UUID para el manejo del identificador


# Esquema para crear una plataforma social
class SocialPlatformCreateModel(BaseModel):
    name: str


# Esquema para actualizar una plataforma social
class SocialPlatformUpdateModel(BaseModel):
    name: Optional[str] = None


# Esquema para la respuesta de una plataforma social (con id UUID)
class SocialPlatformResponseModel(SocialPlatformCreateModel):
    id: UUID  # Usamos UUID para el id de la plataforma social

    class Config:
        orm_mode = True
