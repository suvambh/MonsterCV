from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from use_cases.ports import (
    CVData,
    CVFormParserPort,
    CVOutputGeneratorPort,
    PhotoStoragePort,
)


@dataclass
class SaveCVResult:
    cv_data: CVData
    html_file: Path
    pdf_file: Path
    message: str


def parse_submission_form(
    form: Any,
    parser: CVFormParserPort,
) -> CVData:
    return parser(form)


def generate_cv_artifacts(
    cv_data: CVData,
    output_generator: CVOutputGeneratorPort,
) -> tuple[Path, Path]:
    return output_generator.save_and_generate(cv_data)


def build_save_success_message(
    html_file: Path,
    pdf_file: Path,
) -> str:
    return (
        "CV enregistré avec succès. "
        f"HTML généré: {html_file.name} | PDF généré: {pdf_file.name}"
    )


class EditorWorkflowService:
    """
    Orchestrates editor save workflow.

    Responsibilities:
    - parse submitted form into canonical CV data
    - preserve existing photo if no new upload is provided
    - save new uploaded photo when present
    - trigger HTML/PDF generation
    - return updated CV data plus user-facing message
    """

    def __init__(
        self,
        upload_service: PhotoStoragePort,
        generate_cv_outputs: CVOutputGeneratorPort,
        parse_cv_form_data: CVFormParserPort,
    ) -> None:
        self.upload_service = upload_service
        self.generate_cv_outputs = generate_cv_outputs
        self.parse_cv_form_data = parse_cv_form_data

    def save_submission(
        self,
        form: Any,
        current_cv_data: CVData,
    ) -> SaveCVResult:
        cv_data = parse_submission_form(form, self.parse_cv_form_data)

        photo_file = form.get("photo_file")
        existing_photo_path = current_cv_data.get("photo", "")
        new_photo_path = self.upload_service.save_photo(photo_file)
        cv_data["photo"] = new_photo_path or existing_photo_path

        html_file, pdf_file = generate_cv_artifacts(
            cv_data,
            self.generate_cv_outputs,
        )

        message = build_save_success_message(html_file, pdf_file)

        return SaveCVResult(
            cv_data=cv_data,
            html_file=html_file,
            pdf_file=pdf_file,
            message=message,
        )