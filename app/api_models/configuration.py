from pydantic import BaseModel


# Pydantic model for request validation
class ConfigurationModel(BaseModel):
    key: str
    content: dict
