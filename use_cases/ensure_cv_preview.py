from __future__ import annotations

from pathlib import Path

from use_cases.ports import CVOutputGeneratorPort, CVRepositoryPort


class EnsureCVPreview:
    """Use case for ensuring HTML/PDF preview files exist."""

    def __init__(
        self,
        repository: CVRepositoryPort,
        output_generator: CVOutputGeneratorPort,
        output_dir: Path,
    ) -> None:
        self.repository = repository
        self.output_generator = output_generator
        self.output_dir = output_dir

    def ensure_preview_exists(self) -> tuple[Path, Path]:
        html_file = self.output_dir / "cv_output.html"
        pdf_file = self.output_dir / "cv_output.pdf"

        if html_file.exists() and pdf_file.exists():
            return html_file, pdf_file

        data = self.repository.load()
        return self.output_generator.generate_outputs(data)