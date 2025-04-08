from pydantic import BaseModel
from typing import Optional


class TimelineSectionCreateModel(BaseModel):
    history_id: str
    title: str
    description: Optional[str] = None
    template: Optional[str] = None
    isInverted: bool = False


class TimelineSectionUpdateModel(BaseModel):
    history_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    template: Optional[str] = None
    isInverted: Optional[bool] = None