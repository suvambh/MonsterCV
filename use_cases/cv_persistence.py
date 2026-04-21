# use_cases/cv_persistence.py

from __future__ import annotations

from typing import Any
from infrastructure.cv_repository import CVRepository


class CVPersistence:
    """Use case for loading and saving canonical CV data."""

    def __init__(self, repository: CVRepository) -> None:
        self.repository = repository

    def load_cv(self) -> dict[str, Any]:
        return self.repository.load()

    def save_cv(self, data: dict[str, Any]) -> None:
        self.repository.save(data)