import importlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from db.base import Base
from core.config import settings

POSTGRES_VARIANT = "postgres"
MSSQL_VARIANT = "mssql"

engine = None

if settings.sql_variant == POSTGRES_VARIANT:
    print(f"postgresql+psycopg2://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}")
    engine = create_engine(
        f"postgresql+psycopg2://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}",
        echo=True,
    )

elif settings.sql_variant == MSSQL_VARIANT:
    engine = create_engine(
        f"mssql+pyodbc://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"
        "?driver=ODBC+Driver+17+for+SQL+Server",
        echo=True,
    )

if engine is None:
    raise ValueError("No database variant selected or an invalid SQL variant provided.")


models_directory = Path(__file__).parent / "db_models"
print("Dictitoriy>", models_directory)
for filename in models_directory.glob("*.py"):
    if filename.name != "__init__.py":
        module_name = f"db.db_models.{filename.stem}"
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(
                f"Error importing module {module_name}. Make sure it's properly configured."
            )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
