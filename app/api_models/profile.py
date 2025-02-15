from pydantic import BaseModel, EmailStr
from datetime import datetime


class ProfileCreateModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class ProfileUpdateModel(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    is_active: bool = None

    class Config:
        orm_mode = True
