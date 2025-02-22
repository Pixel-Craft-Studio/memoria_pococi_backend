from fastapi import APIRouter
from fastapi.responses import FileResponse
from services.images_service import get_image, get_folder_size

router = APIRouter()


@router.get("/{prefix}/{folder}/{filename}")
async def get_image_route(prefix: str, folder: str, filename: str):
    file_path = get_image(prefix=prefix, folder=folder, filename=filename)
    return FileResponse(file_path)


@router.get("/monitor")
async def monitor_folder_size():
    total_size = get_folder_size()

    size_in_mb = total_size / (1024 * 1024)

    return {
        "data": {"total_size_in_mb": round(size_in_mb, 2)},
        "message": "Tamaño de la carpeta obtenido exitosamente",
    }
