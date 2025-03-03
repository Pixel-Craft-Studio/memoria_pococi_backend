from pydantic import BaseModel
from typing import Optional


class TimelineCategoryCreateModel(BaseModel):
    name: str

    class Config:
        str_strip_whitespace = True


class TimelineCategoryUpdateModel(BaseModel):
    name: Optional[str] = None

    class Config:
        str_strip_whitespace = True
