from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from services.team_member_service import (
    TeamMemberCreateModel,
    TeamMemberUpdateModel,
    create_team_member,
    get_one_team_member,
    get_all_team_members,
    update_team_member,
    remove_team_member,
)
from core.response_helper import send_response

router = APIRouter()


@router.get("")
def get_team_members(db: Session = Depends(database.get_db)):
    team_members = get_all_team_members(db=db)
    return send_response(
        "Miembros del equipo obtenidos exitosamente",
        [team_member.to_dict() for team_member in team_members],
        200,
    )


@router.get("/{team_member_id}")
def get_team_member(team_member_id: str, db: Session = Depends(database.get_db)):
    team_member = get_one_team_member(db=db, team_member_id=team_member_id)
    if not team_member:
        return send_response("Miembro del equipo no encontrado", status_code=404)
    return send_response(
        "Miembro del equipo obtenido exitosamente", team_member.to_dict(), 200
    )


@router.post("")
def post_team_member(
    team_member: TeamMemberCreateModel, db: Session = Depends(database.get_db)
):
    created_team_member = create_team_member(db=db, team_member=team_member)
    return send_response(
        "Miembro del equipo creado exitosamente", created_team_member.to_dict(), 201
    )


@router.patch("/{team_member_id}")
def patch_team_member(
    team_member_id: str,
    team_member_update: TeamMemberUpdateModel,
    db: Session = Depends(database.get_db),
):
    updated_team_member = update_team_member(
        db=db, team_member_id=team_member_id, team_member_update=team_member_update
    )
    return send_response(
        "Miembro del equipo actualizado exitosamente",
        updated_team_member.to_dict(),
        200,
    )


@router.delete("/{team_member_id}")
def delete_team_member(team_member_id: str, db: Session = Depends(database.get_db)):
    success = remove_team_member(db=db, team_member_id=team_member_id)
    if not success:
        return send_response("Miembro del equipo no encontrado", status_code=404)
    return send_response("Miembro del equipo eliminado exitosamente", status_code=200)
