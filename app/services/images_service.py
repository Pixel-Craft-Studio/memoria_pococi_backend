import os
import shutil

from fastapi import UploadFile, HTTPException
import tempfile
from PIL import Image

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_image(file: UploadFile, prefix: str = "", folder: str = ""):
    save_dir = os.path.join(UPLOAD_DIR, prefix, folder).rstrip("/")
    os.makedirs(save_dir, exist_ok=True)

    file_extension = ".webp" 
    new_filename = f"{folder}{file_extension}"
    final_path = os.path.join(save_dir, new_filename)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        process_image(tmp_path, final_path, 1200, 800)
        os.remove(tmp_path)

    except Exception:
        raise Exception("An error occurred while uploading or processing the image")

    return {
        "filename": new_filename,
        "path": final_path,
        "message": "Image uploaded and processed successfully",
    }


def process_image(input_path, output_path, target_width, target_height):
    with Image.open(input_path) as image:
        image.thumbnail((target_width, target_height), Image.LANCZOS)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path, format="WEBP", quality=85)


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
