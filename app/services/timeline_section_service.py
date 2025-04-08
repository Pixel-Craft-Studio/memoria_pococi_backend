from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.db_models.db_timeline_section import TimelineSection
from api_models.timeline_section import TimelineSectionCreateModel, TimelineSectionUpdateModel
from services.images_service import delete_image, upload_image


def create_timeline_section(db: Session, timeline_section: TimelineSectionCreateModel, image=None):
    custom_id = uuid4()
    image_url = None
    
    if image:
        prefix = "timeline-section"
        folder = str(custom_id)
        file_data = upload_image(image, prefix, folder)
        image_url = f"/{prefix}/{folder}/{file_data.get('filename')}"

    db_timeline_section = TimelineSection(
        id=custom_id,
        history_id=timeline_section.history_id,
        title=timeline_section.title,
        description=timeline_section.description,
        image_url=image_url,
        template=timeline_section.template,
        isInverted=timeline_section.isInverted,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    try:
        db.add(db_timeline_section)
        db.commit()
        db.refresh(db_timeline_section)
        return db_timeline_section
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error al crear la sección en la línea de tiempo: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


def get_one_timeline_section(db: Session, id: str):
    return db.query(TimelineSection).filter(TimelineSection.id == id).first()


def get_all_timeline_sections(db: Session):
    return db.query(TimelineSection).all()


def get_sections_by_history_id(db: Session, history_id: str):
    return db.query(TimelineSection).filter(TimelineSection.history_id == history_id).all()


def update_timeline_section(db: Session, id: str, timeline_section_update: TimelineSectionUpdateModel, image=None):
    db_timeline_section = db.query(TimelineSection).filter(TimelineSection.id == id).first()

    if not db_timeline_section:
        raise ValueError(f"No se encontró la sección {id} en la línea de tiempo")

    if image:
        prefix = "timeline-section"
        folder = str(id)
        delete_image(prefix=prefix, folder=folder)
        file_data = upload_image(image, prefix, folder)
        image_url = f"/{prefix}/{folder}/{file_data.get('filename')}"
        db_timeline_section.image_url = image_url

    if timeline_section_update.history_id:
        db_timeline_section.history_id = timeline_section_update.history_id
    if timeline_section_update.title:
        db_timeline_section.title = timeline_section_update.title
    if timeline_section_update.description:
        db_timeline_section.description = timeline_section_update.description
    if timeline_section_update.template:
        db_timeline_section.template = timeline_section_update.template
    if timeline_section_update.isInverted is not None:
        db_timeline_section.isInverted = timeline_section_update.isInverted

    db_timeline_section.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_timeline_section)
    return db_timeline_section


def remove_timeline_section(db: Session, id: str):
    db_timeline_section = db.query(TimelineSection).filter(TimelineSection.id == id).first()

    if db_timeline_section:
        if db_timeline_section.image_url:
            prefix = "timeline-section"
            folder = str(id)
            delete_image(prefix=prefix, folder=folder)

        db.delete(db_timeline_section)
        db.commit()
        return True
    return False