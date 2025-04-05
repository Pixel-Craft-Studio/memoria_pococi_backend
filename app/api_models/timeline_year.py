from pydantic import BaseModel, Field
from typing import Optional

class TimelineYearCreateModel(BaseModel):
    year: int = Field(...)
    title: str = Field(...)
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(True)

class TimelineYearUpdateModel(BaseModel):
    year: Optional[int] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)
