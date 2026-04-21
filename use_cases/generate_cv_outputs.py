# use_cases/generate_cv_outputs.py

from __future__ import annotations

from pathlib import Path
from typing import Any

from infrastructure.pdf_service import PDFService
from infrastructure.render_service import RenderService
from use_cases.cv_persistence import CVPersistence


class GenerateCVOutputs:
    """Use case for rendering CV HTML and exporting CV PDF."""

    def __init__(
        self,
        persistence: CVPersistence,
        render_service: RenderService,
        pdf_service: PDFService,
        output_dir: Path,
        default_theme: str = "terminal.css",
    ) -> None:
        self.persistence = persistence
        self.render_service = render_service
        self.pdf_service = pdf_service
        self.output_dir = output_dir
        self.default_theme = default_theme

    def generate_outputs(
        self,
        data: dict[str, Any],
        theme_css: str | None = None,
    ) -> tuple[Path, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        html_file = self.output_dir / "cv_output.html"
        pdf_file = self.output_dir / "cv_output.pdf"

        self.render_service.render_and_save(
            data=data,
            output_file=html_file,
            theme_css=theme_css or self.default_theme,
        )
        self.pdf_service.generate_pdf(html_file, pdf_file)

        return html_file, pdf_file

    def save_and_generate(
        self,
        data: dict[str, Any],
        theme_css: str | None = None,
    ) -> tuple[Path, Path]:
        self.persistence.save_cv(data)
        return self.generate_outputs(data, theme_css=theme_css)