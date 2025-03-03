from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.db_models.db_timeline_category import TimelineCategory
from api_models.timeline_category import (
    TimelineCategoryCreateModel,
    TimelineCategoryUpdateModel,
)

def create_timeline_category(db: Session, category: TimelineCategoryCreateModel):
    custom_id = uuid4()

    db_category = TimelineCategory(
        id=custom_id,
        name=category.name,
    )

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe una categoría con el nombre '{category.name}'.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")

# Obtener una categoría por ID
def get_one_timeline_category(db: Session, category_id: UUID):
    return db.query(TimelineCategory).filter(TimelineCategory.id == category_id).first()

# Obtener todas las categorías
def get_all_timeline_categories(db: Session):
    return db.query(TimelineCategory).all()

# Actualizar una categoría
def update_timeline_category(
    db: Session,
    category_id: UUID,
    category_update: TimelineCategoryUpdateModel,
):
    db_category = (
        db.query(TimelineCategory).filter(TimelineCategory.id == category_id).first()
    )

    if not db_category:
        raise ValueError(f"No se encontró la categoría con ID: {category_id}")

    if category_update.name:
        existing_category = (
            db.query(TimelineCategory)
            .filter(TimelineCategory.name == category_update.name)
            .first()
        )

        if existing_category and str(existing_category.id) != str(category_id):
            raise ValueError(f"Ya existe otra categoría con el nombre '{category_update.name}'.")
        
        db_category.name = category_update.name
    
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe una categoría con el nombre '{category_update.name}'.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")

# Eliminar una categoría
def remove_timeline_category(db: Session, category_id: UUID):
    db_category = (
        db.query(TimelineCategory).filter(TimelineCategory.id == category_id).first()
    )

    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False
