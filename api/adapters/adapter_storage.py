import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

from utils.upload import DocumentValidator

class DocumentStorageAdapter:
    def __init__(self, upload_dir: str = "uploads", max_size_mb: int = 5):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.validator = DocumentValidator(max_size=max_size_mb * 1024 * 1024)

    async def save_document(self, file: UploadFile) -> dict[str, object]:
        """Validate file, generate an unique name and save in dest directory."""

        validation = await self.validator.validate_file(file)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail={"message": "File validation failed", "errors": validation["errors"]}
            )

        file_ext = Path(file.filename or "").suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = self.upload_dir / unique_filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )

        return {
            "content_type": file.content_type,
            "size": file.size,
            "location": str(file_path)
        }
