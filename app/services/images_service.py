import os
import shutil
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_image(file: UploadFile, prefix: str = "", folder: str = ""):
    save_dir = os.path.join(UPLOAD_DIR, prefix, folder).rstrip("/")
    os.makedirs(save_dir, exist_ok=True)

    file_extension = os.path.splitext(file.filename)[-1]
    new_filename = f"{folder}{file_extension}"
    file_path = os.path.join(save_dir, new_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        raise Exception("Surgió un error al subir la imagen")

    return {
        "filename": new_filename,
        "path": file_path,
        "message": "Imagen subida exitosamente",
    }


def delete_image(prefix: str = "", folder: str = "", filename: str = ""):
    if not filename:
        folder_path = os.path.join(UPLOAD_DIR, prefix, folder)

        if os.path.exists(folder_path) and os.listdir(folder_path):
            shutil.rmtree(folder_path)
    else:
        file_path = os.path.join(UPLOAD_DIR, prefix, folder, filename)

        if os.path.exists(file_path):
            os.remove(file_path)


def get_image(prefix: str, folder: str, filename: str):
    file_path = os.path.join(UPLOAD_DIR, prefix, folder, filename).rstrip("/")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return file_path


def get_folder_size(prefix: str = "", folder: str = "") -> int:
    folder_path = os.path.join(UPLOAD_DIR, prefix, folder)

    if not os.path.exists(folder_path):
        return 0

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)

    return total_size  