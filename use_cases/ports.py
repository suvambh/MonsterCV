from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

CVData = dict[str, Any]


# --- Repository ---

class CVRepositoryPort(Protocol):
    def load(self) -> CVData: ...
    def save(self, data: CVData) -> None: ...


# --- Rendering ---

class CVRendererPort(Protocol):
    def render(self, data: CVData) -> str: ...


# --- PDF Generation ---

class PDFGeneratorPort(Protocol):
    def generate(self, html_file: Path, pdf_file: Path) -> Path: ...


# --- File Upload / Photo Storage ---

class PhotoStoragePort(Protocol):
    def save_photo(self, photo_file: Any) -> str | None: ...


# --- Output Orchestration (HTML + PDF) ---

class CVOutputGeneratorPort(Protocol):
    def generate_outputs(self, cv_data: CVData) -> tuple[Path, Path]: ...
    def save_and_generate(self, cv_data: CVData) -> tuple[Path, Path]: ...


# --- Form Parsing ---

class CVFormParserPort(Protocol):
    def __call__(self, form: Any) -> CVData: ...