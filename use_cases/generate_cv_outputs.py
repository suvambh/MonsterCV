from __future__ import annotations

from pathlib import Path

from use_cases.ports import CVData, CVRendererPort, CVRepositoryPort, PDFGeneratorPort


class GenerateCVOutputs:
    """Use case for saving CV data, rendering HTML, and exporting PDF."""

    def __init__(
        self,
        repository: CVRepositoryPort,
        renderer: CVRendererPort,
        pdf_generator: PDFGeneratorPort,
        output_dir: Path,
    ) -> None:
        self.repository = repository
        self.renderer = renderer
        self.pdf_generator = pdf_generator
        self.output_dir = output_dir

    def generate_outputs(self, data: CVData) -> tuple[Path, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        html_file = self.output_dir / "cv_output.html"
        pdf_file = self.output_dir / "cv_output.pdf"

        html_content = self.renderer.render(data)
        html_file.write_text(html_content, encoding="utf-8")

        self.pdf_generator.generate(html_file, pdf_file)

        return html_file, pdf_file

    def save_and_generate(self, data: CVData) -> tuple[Path, Path]:
        self.repository.save(data)
        return self.generate_outputs(data)