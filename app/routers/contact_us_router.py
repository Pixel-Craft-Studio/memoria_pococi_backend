from enum import Enum
from typing import List, Optional
from core.login_helper import get_current_user
from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session
from api_models.contact_us import ContactStatus, ContactUpdateRequestModel
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
    contact: ContactUsCreateModel,
    db: Session = Depends(database.get_db),
):
    try:
        created_contact = create_contact_us(db=db, contact=contact)
        send_contact_email(
            contact.name, contact.email, contact.message, contact.subject
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)

    return send_response("Contacto creado exitosamente", created_contact.to_dict(), 201)


@router.get("")
def get_contacts(
    db: Session = Depends(database.get_db),
    status: Optional[ContactStatus] = None,
    current_user: dict = Depends(get_current_user),
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
    contact_id: str = Depends(validate_uuid),
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
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
    current_user: dict = Depends(get_current_user),
):
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


@router.patch("/status/bulk")
def update_multiple_contacts_status_route(
    status: ContactStatus,
    contact_info: ContactUpdateRequestModel,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    updated_contacts = []
    failed_contacts = []

    contact_ids = contact_info.contact_ids

    try:
        for contact_id in contact_ids:
            contact_status_update = ContactUsStatusUpdateModel(status=status)
            updated_contact = update_contact_status(
                db=db,
                contact_id=contact_id,
                contact_status_update=contact_status_update,
            )

            if updated_contact:
                updated_contacts.append(updated_contact.to_dict())
            else:
                failed_contacts.append(contact_id)

        if failed_contacts:
            return send_response(
                "Algunos contactos no fueron encontrados",
                {"actualizados": updated_contacts, "fallidos": failed_contacts},
                207,  # Código 207 indica respuesta mixta
            )

        return send_response(
            "Estados de los contactos actualizados exitosamente",
            updated_contacts,
            200,
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/bulk")
def delete_multiple_contacts_route(
    contact_info: ContactUpdateRequestModel,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    deleted_contacts = []
    failed_contacts = []

    contact_ids = contact_info.contact_ids

    try:
        for contact_id in contact_ids:
            deleted_contact = remove_contact_us(db=db, contact_id=contact_id)

            if deleted_contact:
                deleted_contacts.append(deleted_contact)
            else:
                failed_contacts.append(contact_id)

        if failed_contacts:
            return send_response(
                "Algunos contactos no pudieron ser eliminados",
                {"eliminados": deleted_contacts, "fallidos": failed_contacts},
                207,
            )

        return send_response(
            "Contactos eliminados permanentemente",
            deleted_contacts,
            200,
        )
    except Exception as e:
        return send_response(f"{e}", status_code=400)


@router.delete("/{contact_id}")
def delete_contact_us(
    contact_id: str,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    success = remove_contact_us(db=db, contact_id=contact_id)
    if not success:
        return send_response("Contacto no encontrado", status_code=404)
    return send_response("Contacto eliminado exitosamente", status_code=200)
