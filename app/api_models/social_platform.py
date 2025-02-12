from pydantic import BaseModel

from typing import Optional

# Esquema para crear una plataforma social
class SocialPlatformCreateModel(BaseModel):
    name: str
    icon_url: Optional[str] = None

# Esquema para actualizar una plataforma social
class SocialPlatformUpdateModel(BaseModel):
    name: Optional[str] = None
    icon_url: Optional[str] = None