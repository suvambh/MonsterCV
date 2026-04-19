from __future__ import annotations

from fasthtml.common import *
from monsterui.all import *

from ui_helpers import section_header
from ui_cards import (
    experience_card,
    project_card,
    education_card,
    certification_card,
    skill_card,
)


def general_info_section(data: dict):
    contact = data.get("contact", {})

    return Card(
        Grid(
            LabelInput("Nom", id="name", value=data.get("name", "")),
            LabelInput("Titre", id="title", value=data.get("title", "")),
            Div(
                FormLabel("Photo"),
                Input(
                    type="file",
                    name="photo_file",
                    accept="image/*",
                    onchange="previewPhoto(this)",
                ),
                Div(
                    P("Aperçu", cls=TextPresets.muted_sm),
                    Img(
                        src=data.get("photo", ""),
                        alt="Photo de profil",
                        id="photo-preview",
                        cls=(
                            "w-24 h-24 rounded-full object-cover border"
                            if data.get("photo")
                            else "w-24 h-24 rounded-full object-cover border hidden"
                        ),
                    ),
                    cls="space-y-2",
                ),
                cls="space-y-2",
            ),
            LabelInput("Localisation", id="location", value=data.get("location", "")),
            LabelInput("Email", id="email", name="contact_email", value=contact.get("email", "")),
            LabelInput("Téléphone", id="phone", name="contact_phone", value=contact.get("phone", "")),
            LabelInput("LinkedIn", id="linkedin", name="contact_linkedin", value=contact.get("linkedin", "")),
            LabelInput("GitHub", id="github", name="contact_github", value=contact.get("github", "")),
            cols=2,
        ),
        LabelTextArea("Résumé", id="summary", value=data.get("summary", "")),
        header=section_header(
            "Informations générales",
            "Informations principales et coordonnées.",
        ),
        cls="space-y-6",
    )


def action_bar():
    return DivRAligned(
        Button("Enregistrer", cls=ButtonT.primary, type="submit"),
        cls="pt-2",
    )


def repeatable_section(
    title: str,
    subtitle: str,
    list_id: str,
    empty_text: str,
    items: list[dict],
    item_renderer,
    add_url: str,
    add_label: str,
):
    rendered_items = [item_renderer(item) for item in items]

    content = [Div(*rendered_items, id=list_id, cls="space-y-4")]

    if not items:
        content.insert(0, P(empty_text, cls=TextPresets.muted_sm))

    content.append(
        Button(
            add_label,
            cls=ButtonT.secondary,
            type="button",
            hx_get=add_url,
            hx_target=f"#{list_id}",
            hx_swap="beforeend",
        )
    )

    return Card(
        *content,
        header=section_header(title, subtitle),
        cls="space-y-4",
    )


def build_form_sections(data: dict):
    return (
        general_info_section(data),
        repeatable_section(
            "Compétences",
            "Liste structurée des compétences.",
            "skills-list",
            "Aucune compétence ajoutée.",
            data.get("skills", []),
            skill_card,
            "/editor/skill/new",
            "Ajouter une catégorie de compétences",
        ),
        repeatable_section(
            "Expérience",
            "Ajoute une ou plusieurs expériences professionnelles.",
            "experience-list",
            "Aucune expérience ajoutée.",
            data.get("experience", []),
            experience_card,
            "/editor/experience/new",
            "Ajouter une expérience",
        ),
        repeatable_section(
            "Projets",
            "Ajoute les projets à mettre en avant.",
            "project-list",
            "Aucun projet ajouté.",
            data.get("projects", []),
            project_card,
            "/editor/project/new",
            "Ajouter un projet",
        ),
        repeatable_section(
            "Formation",
            "Ajoute les études et diplômes.",
            "education-list",
            "Aucune formation ajoutée.",
            data.get("education", []),
            education_card,
            "/editor/education/new",
            "Ajouter une formation",
        ),
        repeatable_section(
            "Certifications",
            "Ajoute les certifications pertinentes.",
            "cert-list",
            "Aucune certification ajoutée.",
            data.get("certifications", []),
            certification_card,
            "/editor/certification/new",
            "Ajouter une certification",
        ),
    )