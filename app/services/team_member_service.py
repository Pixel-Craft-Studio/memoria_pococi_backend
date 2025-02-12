import uuid
from sqlalchemy.orm import Session
from db_models.db_team_member_models import SocialMedia, TeamMember
from api_models.team_member import TeamMemberCreateModel, TeamMemberUpdateModel
from sqlalchemy.exc import IntegrityError

# Crear un nuevo miembro del equipo
def create_team_member(db: Session, team_member: TeamMemberCreateModel):
    # Generamos un ID único para el miembro del equipo
    member_id = str(uuid.uuid4())
    
    # Creamos el objeto TeamMember
    db_team_member = TeamMember(
        id=member_id,
        name=team_member.name,
        photo_url=team_member.photo_url,
        description=team_member.description,
        role=team_member.role,
    )
    
    try:
        # Agregamos el miembro del equipo
        db.add(db_team_member)
        
        # Si hay redes sociales, las creamos
        if hasattr(team_member, 'social_media') and team_member.social_media:
            for social in team_member.social_media:
                social_media = SocialMedia(
                    id=str(uuid.uuid4()),
                    team_member_id=member_id,
                    platform_id=social.platform_id,
                    url=social.url
                )
                db.add(social_media)
        
        # Confirmamos la transacción
        db.commit()
        db.refresh(db_team_member)
        return db_team_member
        
    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            f"Error al crear el miembro del equipo. Error de integridad: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise Exception(f"Error inesperado: {str(e)}")


# Obtener un miembro del equipo por ID
def get_one_team_member(db: Session, team_member_id: str):
    return db.query(TeamMember).filter(TeamMember.id == team_member_id).first()


# Obtener todos los miembros del equipo
def get_all_team_members(db: Session):
    return db.query(TeamMember).all()


# Actualizar un miembro del equipo
def update_team_member(
    db: Session, team_member_id: str, team_member_update: TeamMemberUpdateModel
):
    db_team_member = (
        db.query(TeamMember).filter(TeamMember.id == team_member_id).first()
    )

    if not db_team_member:
        raise ValueError(
            f"No se encontró el miembro del equipo con ID: {team_member_id}"
        )

    # Actualizamos los campos proporcionados
    if team_member_update.name:
        db_team_member.name = team_member_update.name
    if team_member_update.photo_url:
        db_team_member.photo_url = team_member_update.photo_url
    if team_member_update.description:
        db_team_member.description = team_member_update.description
    if team_member_update.role:
        db_team_member.role = team_member_update.role

    # Si hay redes sociales, las actualizamos
    if hasattr(team_member_update, 'social_media') and team_member_update.social_media:
        # Primero, eliminamos las redes sociales existentes para este miembro del equipo
        db.query(SocialMedia).filter(SocialMedia.team_member_id == team_member_id).delete()
        
        # Luego, agregamos las nuevas redes sociales
        for social in team_member_update.social_media:
            social_media = SocialMedia(
                id=str(uuid.uuid4()),
                team_member_id=team_member_id,
                platform_id=social.platform_id,
                url=social.url
            )
            db.add(social_media)

    db.commit()
    db.refresh(db_team_member)
    return db_team_member


# Eliminar un miembro del equipo
def remove_team_member(db: Session, team_member_id: str):
    db_team_member = (
        db.query(TeamMember).filter(TeamMember.id == team_member_id).first()
    )

    if db_team_member:
        db.delete(db_team_member)
        db.commit()
        return True
    return False
