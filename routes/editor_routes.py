from __future__ import annotations

from adapters.cv_loader import load_cv_json_from_bytes
from adapters.cv_form_parser import parse_cv_form_data
from dependencies import generate_cv_outputs
from domain.cv_schema import empty_cv
from infrastructure.upload_service import UploadService
from ui.editor_page import editor_page
from ui.ui_cards import (
    experience_card,
    project_card,
    education_card,
    certification_card,
    skill_card,
)
from use_cases.editor_workflow_service import EditorWorkflowService


CURRENT_CV_DATA = empty_cv()

upload_service = UploadService()
save_workflow = EditorWorkflowService(
    upload_service=upload_service,
    generate_cv_outputs=generate_cv_outputs,
    parse_cv_form_data=parse_cv_form_data,
)


def register_editor_routes(rt):
    @rt("/")
    def index():
        return editor_page(CURRENT_CV_DATA)

    @rt("/load-json", methods=["POST"])
    async def load_json(request):
        global CURRENT_CV_DATA

        try:
            form = await request.form()
            cv_json_file = form.get("cv_json_file")

            if cv_json_file is None or not getattr(cv_json_file, "filename", ""):
                return editor_page(CURRENT_CV_DATA, "Aucun fichier fourni.", error=True)

            content = await cv_json_file.read()
            CURRENT_CV_DATA = load_cv_json_from_bytes(content)
            return editor_page(CURRENT_CV_DATA, "Fichier JSON chargé avec succès.")

        except Exception as e:
            return editor_page(
                CURRENT_CV_DATA,
                f"Erreur lors du chargement du JSON : {type(e).__name__}: {e}",
                error=True,
            )

    @rt("/save", methods=["POST"])
    async def save_cv(request):
        global CURRENT_CV_DATA

        try:
            form = await request.form()

            result = save_workflow.save_submission(form, CURRENT_CV_DATA)
            CURRENT_CV_DATA = result.cv_data

            return editor_page(CURRENT_CV_DATA, result.message)

        except Exception as e:
            return editor_page(
                CURRENT_CV_DATA,
                f"Erreur lors de l'enregistrement/génération : {type(e).__name__}: {e}",
                error=True,
            )

    @rt("/editor/experience/new")
    def editor_experience_new():
        return experience_card({})

    @rt("/editor/project/new")
    def editor_project_new():
        return project_card({})

    @rt("/editor/education/new")
    def editor_education_new():
        return education_card({})

    @rt("/editor/certification/new")
    def editor_certification_new():
        return certification_card({})

    @rt("/editor/skill/new")
    def editor_skill_new():
        return skill_card({})