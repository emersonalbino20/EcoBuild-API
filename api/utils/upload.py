from pathlib import Path
from typing import TypedDict

from fastapi import UploadFile


class ValidationResult(TypedDict):
    valid: bool
    errors: list[str]


class DocumentValidator:
    def __init__(self, max_size: int = 10 * 1024 * 1024):
        self.max_size = max_size
        self.allowed_extensions = {'.pdf', '.txt', '.json'}

    async def validate_file(self, file: UploadFile) -> ValidationResult:
        result: ValidationResult = {"valid": True, "errors": []}
        
        if not file.filename or file.filename.strip() == "":
            result["valid"] = False
            result["errors"].append("No file selected")
            return result
      
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            result["valid"] = False
            result["errors"].append(
               f"File extension '{file_ext}' not allowed. Use: .pdf, .txt, .json"
            )
         
        content = await file.read()
        await file.seek(0) # Reset file pointer for later use

        file_size = len(content)
        if file_size > self.max_size:
            result["valid"] = False
            result["errors"].append(
                f"File too large ({file_size:,} bytes). Maximum: {self.max_size:,} bytes"
            )

        return result
        
