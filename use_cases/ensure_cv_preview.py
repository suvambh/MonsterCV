# use_cases/ensure_cv_preview.py

from __future__ import annotations

from pathlib import Path

from use_cases.cv_persistence import CVPersistence
from use_cases.generate_cv_outputs import GenerateCVOutputs


class EnsureCVPreview:
    """Use case for ensuring HTML/PDF preview files exist."""

    def __init__(
        self,
        persistence: CVPersistence,
        output_generator: GenerateCVOutputs,
        output_dir: Path,
    ) -> None:
        self.persistence = persistence
        self.output_generator = output_generator
        self.output_dir = output_dir

    def ensure_preview_exists(self, theme_css: str | None = None) -> tuple[Path, Path]:
        html_file = self.output_dir / "cv_output.html"
        pdf_file = self.output_dir / "cv_output.pdf"

        if html_file.exists() and pdf_file.exists():
            return html_file, pdf_file

        data = self.persistence.load_cv()
        return self.output_generator.generate_outputs(data, theme_css=theme_css)