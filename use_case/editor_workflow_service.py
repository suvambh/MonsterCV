# editor_workflow_service.py

from dataclasses import dataclass
from typing import Any


@dataclass
class SaveCVResult:
    cv_data: dict[str, Any]
    html_file: Any
    pdf_file: Any
    message: str


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

    def __init__(self, upload_service, cv_service, parse_cv_form_data):
        self.upload_service = upload_service
        self.cv_service = cv_service
        self.parse_cv_form_data = parse_cv_form_data

    def save_submission(self, form, current_cv_data: dict[str, Any]) -> SaveCVResult:
        cv_data = self.parse_cv_form_data(form)

        photo_file = form.get("photo_file")
        existing_photo_path = current_cv_data.get("photo", "")
        new_photo_path = self.upload_service.save_photo(photo_file)

        cv_data["photo"] = new_photo_path or existing_photo_path

        html_file, pdf_file = self.cv_service.save_and_generate(cv_data)

        message = (
            f"CV enregistré avec succès. "
            f"HTML généré: {html_file.name} | PDF généré: {pdf_file.name}"
        )

        return SaveCVResult(
            cv_data=cv_data,
            html_file=html_file,
            pdf_file=pdf_file,
            message=message,
        )