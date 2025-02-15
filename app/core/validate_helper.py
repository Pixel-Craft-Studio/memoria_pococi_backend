from uuid import UUID
from fastapi import HTTPException




def validate_uuid(platform_id: str) -> str:
    try:
        UUID(platform_id)
        return platform_id
    except ValueError:
        raise HTTPException(status_code=400, detail= "El id no es válido")
