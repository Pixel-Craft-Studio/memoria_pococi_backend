from pydantic import BaseModel

class RecoveryCreateModel(BaseModel):
    email: str


class ResetCreateModel(BaseModel):
    password: str
