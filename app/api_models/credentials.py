from pydantic import BaseModel

class RecoveryCreateModel(BaseModel):
    email: str


class ResetCreateModel(BaseModel):
    profile_id: str
    currentPassword: str
    password: str
