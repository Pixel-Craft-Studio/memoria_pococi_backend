from pydantic import BaseModel
import enum

class ContactStatus(enum.Enum):
    NEW = "new"
    READ = "readed"
    ARCHIVED = "archived"
    RESPONDED = "responded"
    DELETED = "deleted"

class ContactUsCreateModel(BaseModel):
    name: str
    email: str
    message: str
    subject: str  

    class Config:
        str_strip_whitespace = True

class ContactUsStatusUpdateModel(BaseModel):
    status: ContactStatus  

    class Config:
        str_strip_whitespace = True
