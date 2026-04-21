from __future__ import annotations

from pathlib import Path
from infrastructure.pdf_service import PDFService
from typing import Any
from use_cases.ports import CVData


class PDFServiceAdapter:
    def __init__(self, pdf_service: PDFService) -> None:
        self.pdf_service = pdf_service

    def generate(self, html_file: Path, pdf_file: Path) -> Path:
        return self.pdf_service.generate_pdf(html_file, pdf_file)



class RenderServiceAdapter:
    def __init__(self, render_service: Any) -> None:
        self.render_service = render_service

    def render(self, data: CVData) -> str:
        return self.render_service.render_cv_html(data)