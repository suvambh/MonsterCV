# use_cases/cv_persistence.py

from __future__ import annotations

from typing import Any

from domain.cv_schema import empty_cv
from infrastructure.json_repository import JSONRepository


class CVPersistence:
    """Use case for loading and saving canonical CV data."""

    def __init__(self, repository: JSONRepository) -> None:
        self.repository = repository

    def load_cv(self) -> dict[str, Any]:
        data = self.repository.load()
        if data is None:
            data = empty_cv()
        return data


    def save_cv(self, data: dict[str, Any]) -> None:
        self.repository.save(data)