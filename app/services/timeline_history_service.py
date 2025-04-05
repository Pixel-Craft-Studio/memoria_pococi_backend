from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.db_models.db_timeline_history import TimelineHistory
from api_models.timeline_history import TimelineHistoryCreateModel, TimelineHistoryUpdateModel
from services.images_service import delete_image, upload_image


def create_timeline_history(db: Session, timeline_history: TimelineHistoryCreateModel, image):
    custom_id = uuid4()
    prefix = "timeline-history"
    folder = str(custom_id)
    file_data = upload_image(image, prefix, folder)
    image_url = f"/{prefix}/{folder}/{file_data.get('filename')}"

    db_timeline_history = TimelineHistory(
        id=custom_id,
        title=timeline_history.title,
        description=timeline_history.description,
        image_url=image_url, 
        timeline_id=timeline_history.timeline_id,
        event_date=timeline_history.event_date,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    try:
        db.add(db_timeline_history)
        db.commit()
        db.refresh(db_timeline_history)
        return db_timeline_history
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error al crear la historia en la línea de tiempo: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


def get_one_timeline_history(db: Session, history_id: UUID):
    return db.query(TimelineHistory).filter(TimelineHistory.id == history_id).first()


def get_all_timeline_histories(db: Session):
    return db.query(TimelineHistory).all()


def update_timeline_history(db: Session, history_id: UUID, timeline_history_update: TimelineHistoryUpdateModel, image=None):
    db_timeline_history = db.query(TimelineHistory).filter(TimelineHistory.id == history_id).first()

    if not db_timeline_history:
        raise ValueError(f"No se encontró la historia con ID {history_id} en la línea de tiempo")

    if image:
        prefix = "timeline-history"
        folder = str(db_timeline_history.id)
        delete_image(prefix=prefix, folder=folder)
        file_data = upload_image(image, prefix, folder)
        image_url = f"/{prefix}/{folder}/{file_data.get('filename')}"
        db_timeline_history.image_url = image_url

    if timeline_history_update.title:
        db_timeline_history.title = timeline_history_update.title
    if timeline_history_update.description:
        db_timeline_history.description = timeline_history_update.description
    if timeline_history_update.status is not None:
        db_timeline_history.status = timeline_history_update.status
    if timeline_history_update.event_date:
        db_timeline_history.event_date = timeline_history_update.event_date

    db_timeline_history.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_timeline_history)
    return db_timeline_history


def remove_timeline_history(db: Session, history_id: UUID):
    db_timeline_history = db.query(TimelineHistory).filter(TimelineHistory.id == history_id).first()

    if db_timeline_history:
        prefix = "timeline-history"
        folder = str(db_timeline_history.timeline_id)
        delete_image(prefix=prefix, folder=folder)

        db.delete(db_timeline_history)
        db.commit()
        return True
    return False


def remove_timeline_history_by_year_id(db: Session, year_id: UUID):
    histories = db.query(TimelineHistory).filter(TimelineHistory.timeline_id == year_id).all()  # Obtener lista

    if histories:
        prefix = "timeline-history"

        for history in histories:
            history_dict = history.to_dict()
            print("Dictionario", history_dict)
            print("Historiadas", history_dict.get("id"))
            
            folder = str(history_dict.get("id"))
            delete_image(prefix=prefix, folder=folder)

            db.delete(history)

        db.commit()
        return True
    
    return False
