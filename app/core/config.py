from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_port: str 
    db_name: str 

    class Config:
        env_file = ".env"


settings = Settings()
