from __future__ import annotations

from fasthtml.common import *
from monsterui.all import *

from cv_loader import load_cv_json_from_bytes
from ui_helpers import page_scripts, message_alert, section_header
from ui_sections import build_form_sections, action_bar
from ui_cards import (
    experience_card,
    project_card,
    education_card,
    certification_card,
    skill_card,
)

from cv_form_parser import parse_cv_form_data
from cv_services import cv_service
from cv_schema import empty_cv


app, rt = fast_app(hdrs=Theme.blue.headers())


# --------------------------------------------------
# In-memory state for demo purposes
# Replace later with session/db/persistence if needed
# --------------------------------------------------

CURRENT_CV_DATA = empty_cv()

# --------------------------------------------------
# Top upload section
# --------------------------------------------------

def upload_json_section():
    return Card(
        Form(
            LabelInput(
                "Nom du fichier JSON (optionnel)",
                id="json_filename",
                value="",
                placeholder="data.json",
                disabled=True,
            ),
            Div(
                FormLabel("Choisir un fichier JSON"),
                Input(type="file", name="cv_json_file", accept=".json,application/json"),
                cls="space-y-2",
            ),
            DivRAligned(
                Button("Charger le fichier JSON", cls=ButtonT.primary, type="submit"),
            ),
            method="post",
            action="/load-json",
            enctype="multipart/form-data",
            cls="space-y-4",
        ),
        header=section_header(
            "Importer un CV JSON",
            "Charge un fichier JSON puis remplit automatiquement le formulaire.",
        ),
    )


# --------------------------------------------------
# Main page
# --------------------------------------------------

def editor_page(data: dict, message: str | None = None, error: bool = False):
    return (
        Title("Éditeur du CV"),
        page_scripts(),
        Container(
            Div(
                H2("Éditeur du CV"),
                Subtitle("Charge un fichier JSON puis modifie les champs."),
                cls="space-y-2 mb-8",
            ),
            upload_json_section(),
            message_alert(message, error),
            Form(
                *build_form_sections(data),
                action_bar(),
                method="post",
                action="/save",
                cls="space-y-6",
            ),
            cls="max-w-5xl space-y-6",
        ),
    )


# --------------------------------------------------
# Routes
# --------------------------------------------------

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

        # --- HANDLE PHOTO UPLOAD ---
        photo_file = form.get("photo_file")

        photo_path = CURRENT_CV_DATA.get("photo", "")

        if photo_file and getattr(photo_file, "filename", ""):
            upload_dir = Path("static/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)

            file_path = upload_dir / photo_file.filename

            with open(file_path, "wb") as f:
                f.write(await photo_file.read())

            photo_path = f"/static/uploads/{photo_file.filename}"



        # --- PARSE FORM ---
        CURRENT_CV_DATA = parse_cv_form_data(form)

        # inject uploaded photo path
        CURRENT_CV_DATA["photo"] = photo_path

        html_file, pdf_file = cv_service.save_and_generate(CURRENT_CV_DATA)

        message = (
            f"CV enregistré avec succès. "
            f"HTML généré: {html_file.name} | PDF généré: {pdf_file.name}"
        )
        return editor_page(CURRENT_CV_DATA, message)

    except Exception as e:
        return editor_page(
            CURRENT_CV_DATA,
            f"Erreur lors de l'enregistrement/génération : {type(e).__name__}: {e}",
            error=True,
        )




# --------------------------------------------------
# HTMX fragment endpoints for adding new items
# --------------------------------------------------

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


serve()