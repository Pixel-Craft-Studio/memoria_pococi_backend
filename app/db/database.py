from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models.db_team_member_models import TeamMember, SocialMedia, SocialPlatform
from db_models.db_configuration_models import Configuration
from db_models.db_base import Base
from core.config import settings

engine = create_engine(
    f"mssql+pyodbc://{settings.db_user}:{settings.db_pass}@{settings.db_host},{settings.db_port}/{settings.db_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server",
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
