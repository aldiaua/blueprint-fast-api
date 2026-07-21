import uuid
from pathlib import Path
from typing import Dict

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.config.settings import settings

# --- Configuration for Media Uploads ---
MAX_FILE_SIZE_MB = 5
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}


class MediaService:
    """
    A straightforward service to handle media uploads to local storage.
    """

    def __init__(self, base_path: str = settings.LOCAL_STORAGE_PATH):
        self.base_path = Path(base_path)
        self.base_url = f"/{base_path.strip('./')}"
        # Ensure the base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_file(
        self, file: UploadFile, sub_folder: str = "images"
    ) -> Dict[str, any]:
        # 1. Validate file presence
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided."
            )

        # 2. Validate MIME type (security)
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type '{file.content_type}' is not allowed.",
            )

        # 3. Generate a unique filename to prevent overwrites and path traversal attacks
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # 4. Create destination path
        destination_dir = self.base_path / sub_folder
        destination_dir.mkdir(parents=True, exist_ok=True)
        file_path = destination_dir / unique_filename

        # 5. Read file content, validate size, and save it asynchronously
        content = await file.read()
        if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds the limit of {MAX_FILE_SIZE_MB} MB.",
            )

        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(content)

        # 6. Return public URL and metadata
        return {
            "url": f"{self.base_url}/{sub_folder}/{unique_filename}",
            "filename": file.filename,
            "content_type": file.content_type,
            "size_kb": len(content) / 1024,
        }