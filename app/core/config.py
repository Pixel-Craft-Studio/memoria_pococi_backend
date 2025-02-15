from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_port: str 
    db_name: str 

    api_secret_key: str 
    access_token_expire_hours: int 
    secret_algorithm: str 
    pepper: str

    class Config:
        env_file = ".env"


settings = Settings()
