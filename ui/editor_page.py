from __future__ import annotations

from fasthtml.common import *
from monsterui.all import *

from ui.ui_helpers import page_scripts, message_alert, section_header
from ui.ui_sections import build_form_sections, action_bar


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