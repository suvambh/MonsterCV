# upload_service.py

from pathlib import Path
import os
import uuid


class UploadService:
    """
    Handles file uploads (currently photo uploads for CV).
    Responsible ONLY for saving files and returning browser paths.
    """

    def __init__(self, upload_dir: str = "static/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_photo(self, uploaded_file) -> str:
        """
        Save uploaded file and return browser path.
        """

        # No file uploaded
        if not uploaded_file or not getattr(uploaded_file, "filename", ""):
            return ""

        # Extract extension
        ext = os.path.splitext(uploaded_file.filename)[1].lower()

        # Generate unique filename
        filename = f"{uuid.uuid4().hex}{ext}"
        output_path = self.upload_dir / filename

        # Save file
        with open(output_path, "wb") as f:
            f.write(uploaded_file.file.read())

        # Return browser path (IMPORTANT invariant)
        return f"/static/uploads/{filename}"