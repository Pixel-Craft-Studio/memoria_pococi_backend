from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.db_models.db_timeline_year import TimelineYear
from api_models.timeline_year import TimelineYearCreateModel, TimelineYearUpdateModel
from services.images_service import delete_image, upload_image


def create_timeline_year(db: Session, timeline_year: TimelineYearCreateModel, image):
    custom_id = uuid4()
    prefix = "timeline-year"
    folder = str(custom_id)
    file_data = upload_image(image, prefix, folder)
    image_url = f"/{prefix}/{folder}/{file_data.get('filename')}"

    db_timeline_year = TimelineYear(
        id=custom_id,
        year=timeline_year.year,
        title=timeline_year.title,
        description=timeline_year.description,
        image_url=image_url,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_active=True,
    )

    try:
        db.add(db_timeline_year)
        db.commit()
        db.refresh(db_timeline_year)
        return db_timeline_year
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error al crear el año en la línea de tiempo: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


def get_one_timeline_year(db: Session, id: str):
    return db.query(TimelineYear).filter(TimelineYear.id == id).first()

def get_one_timeline_year_by_year(db: Session, year: str):
    return db.query(TimelineYear).filter(TimelineYear.year == year).first()

def get_all_timeline_years(db: Session):
    return db.query(TimelineYear).order_by(TimelineYear.year.asc()).all()


def update_timeline_year(db: Session, id:str, timeline_year_update: TimelineYearUpdateModel, image=None):
    db_timeline_year = db.query(TimelineYear).filter(TimelineYear.id == id).first()

    if not db_timeline_year:
        raise ValueError(f"No se encontró el año {id} en la línea de tiempo")

    if image:
        prefix = "timeline-year"
        folder = str(id)
        delete_image(prefix=prefix, folder=folder)
        file_data = upload_image(image, prefix, folder)
        image_url = f"/{prefix}/{folder}/{file_data.get('filename')}"
        db_timeline_year.image_url = image_url

    if timeline_year_update.year:
        db_timeline_year.year = timeline_year_update.year
    if timeline_year_update.title:
        db_timeline_year.title = timeline_year_update.title
    if timeline_year_update.description:
        db_timeline_year.description = timeline_year_update.description
    if timeline_year_update.is_active is not None:
        db_timeline_year.is_active = timeline_year_update.is_active

    db_timeline_year.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_timeline_year)
    return db_timeline_year


def remove_timeline_year(db: Session, id: str):
    db_timeline_year = db.query(TimelineYear).filter(TimelineYear.id == id).first()

    if db_timeline_year:
        prefix = "timeline-year"
        folder = str(id)
        delete_image(prefix=prefix, folder=folder)

        db.delete(db_timeline_year)
        db.commit()
        return True
    return False
