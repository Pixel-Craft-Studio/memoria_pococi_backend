from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from api_models.contact_us import ContactStatus
from db import database
from services.contact_us_service import (
    create_contact_us,
    get_all_contacts,
    get_one_contact,
    update_contact_status,
    remove_contact_us,
)
from core.response_helper import send_response
from services.email_service import send_contact_email  
from api_models.contact_us import ContactUsCreateModel, ContactUsStatusUpdateModel
from core.validate_helper import validate_uuid

router = APIRouter()


@router.post("")
async def post_contact_us(
    contact: ContactUsCreateModel, db: Session = Depends(database.get_db)
):
    try:
        created_contact = create_contact_us(db=db, contact=contact)
        send_contact_email(contact.name, contact.email, contact.message, contact.subject)
    except Exception as e:
        return send_response(f"{e}", status_code=400)

    return send_response("Contacto creado exitosamente", created_contact.to_dict(), 201)


@router.get("")
def get_contacts(
    db: Session = Depends(database.get_db), status: Optional[ContactStatus] = None
):
    if status:
        status = status

    contacts = get_all_contacts(db=db, status=status)
    return send_response(
        "Contactos obtenidos exitosamente",
        [contact.to_dict() for contact in contacts],
        200,
    )


@router.get("/{contact_id}")
def get_contact(
    contact_id: str = Depends(validate_uuid), db: Session = Depends(database.get_db)
):
    contact = get_one_contact(db=db, contact_id=contact_id)

    if not contact:
        return send_response("Contacto no encontrado", status_code=404)
    return send_response("Contacto obtenido exitosamente", contact.to_dict(), 200)


@router.patch("/{contact_id}/status")
def update_contact_status_route(
    contact_id: str,
    status: Optional[ContactStatus] = None,
    db: Session = Depends(database.get_db),
):
    if status and status not in ContactStatus.__members__:
        return {"message": "Estado no válido", "status_code": 404}

    contact_status_update = ContactUsStatusUpdateModel(status=status)

    try:
        updated_contact = update_contact_status(
            db=db, contact_id=contact_id, contact_status_update=contact_status_update
        )
        if not updated_contact:
            return send_response("Contacto no encontrado", status_code=404)
        return send_response(
            "Estado del contacto actualizado exitosamente",
            updated_contact.to_dict(),
            200,
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/{contact_id}")
def delete_contact_us(contact_id: str, db: Session = Depends(database.get_db)):
    success = remove_contact_us(db=db, contact_id=contact_id)
    if not success:
        return send_response("Contacto no encontrado", status_code=404)
    return send_response("Contacto eliminado exitosamente", status_code=200)
