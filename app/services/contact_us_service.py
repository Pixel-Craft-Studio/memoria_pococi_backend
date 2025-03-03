from typing import List, Optional
from sqlalchemy.orm import Session
from db.db_models.db_contact_us import ContactUs
from api_models.contact_us import ContactUsCreateModel, ContactUsStatusUpdateModel
from sqlalchemy.exc import IntegrityError
from uuid import UUID


def create_contact_us(db: Session, contact: ContactUsCreateModel) -> ContactUs:
    try:
        new_contact = ContactUs(
            name=contact.name,
            email=contact.email,
            message=contact.message,
            subject=contact.subject,
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
    except IntegrityError:
        db.rollback()
        raise ValueError("Surgió un error al registrar")


def get_all_contacts(db: Session, status: Optional[str] = None) -> List[ContactUs]:
    query = db.query(ContactUs)
    if status:
        query = query.filter(ContactUs.status == status)
    return query.all()


def get_one_contact(db: Session, contact_id: UUID) -> Optional[ContactUs]:
    return db.query(ContactUs).filter(ContactUs.id == contact_id).first()


def update_contact_status(
    db: Session, contact_id: UUID, contact_status_update: ContactUsStatusUpdateModel
) -> Optional[ContactUs]:
    contact = db.query(ContactUs).filter(ContactUs.id == contact_id).first()
    if contact:
        contact.status = contact_status_update.status
        db.commit()
        db.refresh(contact)
        return contact
    return None


def remove_contact_us(db: Session, contact_id: UUID) -> bool:
    contact = db.query(ContactUs).filter(ContactUs.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
        return True
    return False
