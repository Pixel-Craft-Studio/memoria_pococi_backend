from pydantic import BaseModel
from typing import Optional, List, Any


class TeamMemberBaseModel(BaseModel):
    name: str
    photo_url: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None


class SocialMediaCreate(BaseModel):
    platform_id: str
    url: str


class TeamMemberCreateModel(TeamMemberBaseModel):
    social_media: Optional[List[SocialMediaCreate]] = None


class TeamMemberUpdateModel(TeamMemberBaseModel):
    pass


class TeamMemberResponseModel(TeamMemberBaseModel):
    id: str

    class Config:
        orm_mode = True
