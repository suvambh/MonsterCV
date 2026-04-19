from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CVRepository:
    """Simple JSON file repository for CV data."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load(self) -> dict[str, Any]:
        if not self.file_path.exists():
            return {
                "name": "",
                "title": "",
                "photo": "",
                "location": "",
                "summary": "",
                "contact": {
                    "email": "",
                    "phone": "",
                    "linkedin": "",
                    "github": "",
                },
                "skills": [],
                "experience": [],
                "projects": [],
                "education": [],
                "certifications": [],
            }

        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: dict[str, Any]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)