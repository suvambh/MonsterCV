from __future__ import annotations

from fasthtml.common import *
from monsterui.all import *

from ui_helpers import text_value, textarea_value, list_to_csv


def experience_card(item: dict | None = None):
    item = item or {}
    return Div(
        Card(
            Grid(
                LabelInput("Poste", id="", name="experience_role[]", value=text_value(item, "role")),
                LabelInput("Entreprise", id="", name="experience_company[]", value=text_value(item, "company")),
                LabelInput("Durée", id="", name="experience_duration[]", value=text_value(item, "duration")),
                LabelInput("Lieu", id="", name="experience_location[]", value=text_value(item, "location")),
                cols=2,
            ),
            LabelInput("Technologies", id="", name="experience_tech[]", value=text_value(item, "tech")),
            LabelTextArea(
                "Détails (une ligne = un bullet)",
                id="",
                name="experience_details[]",
                value=textarea_value(item, "details"),
            ),
            header=DivFullySpaced(
                H4("Expérience"),
                Button(
                    "Supprimer",
                    cls=ButtonT.destructive,
                    type="button",
                    onclick="removeItem(this)",
                ),
            ),
            cls="space-y-4",
        ),
        cls="repeatable-item",
    )


def project_card(item: dict | None = None):
    item = item or {}
    return Div(
        Card(
            LabelInput("Nom", id="", name="project_name[]", value=text_value(item, "name")),
            LabelInput("Technologies", id="", name="project_tech[]", value=text_value(item, "tech")),
            LabelTextArea(
                "Détails (une ligne = un bullet)",
                id="",
                name="project_details[]",
                value=textarea_value(item, "details"),
            ),
            header=DivFullySpaced(
                H4("Projet"),
                Button(
                    "Supprimer",
                    cls=ButtonT.destructive,
                    type="button",
                    onclick="removeItem(this)",
                ),
            ),
            cls="space-y-4",
        ),
        cls="repeatable-item",
    )


def education_card(item: dict | None = None):
    item = item or {}
    return Div(
        Card(
            Grid(
                LabelInput("Diplôme", id="", name="education_degree[]", value=text_value(item, "degree")),
                LabelInput("Institution", id="", name="education_institution[]", value=text_value(item, "institution")),
                LabelInput("Lieu", id="", name="education_location[]", value=text_value(item, "location")),
                LabelInput("Année / période", id="", name="education_year[]", value=text_value(item, "year")),
                cols=2,
            ),
            header=DivFullySpaced(
                H4("Formation"),
                Button(
                    "Supprimer",
                    cls=ButtonT.destructive,
                    type="button",
                    onclick="removeItem(this)",
                ),
            ),
            cls="space-y-4",
        ),
        cls="repeatable-item",
    )


def certification_card(item: dict | None = None):
    item = item or {}
    return Div(
        Card(
            Grid(
                LabelInput("Nom", id="", name="cert_name[]", value=text_value(item, "name")),
                LabelInput("Organisme", id="", name="cert_issuer[]", value=text_value(item, "issuer")),
                LabelInput("Année", id="", name="cert_year[]", value=text_value(item, "year")),
                cols=2,
            ),
            header=DivFullySpaced(
                H4("Certification"),
                Button(
                    "Supprimer",
                    cls=ButtonT.destructive,
                    type="button",
                    onclick="removeItem(this)",
                ),
            ),
            cls="space-y-4",
        ),
        cls="repeatable-item",
    )


def skill_card(item: dict | None = None):
    item = item or {}
    return Div(
        Card(
            LabelInput("Catégorie", id="", name="skill_category[]", value=text_value(item, "category")),
            LabelInput(
                "Compétences (séparées par des virgules)",
                id="",
                name="skill_items[]",
                value=list_to_csv(item.get("items", [])),
            ),
            header=DivFullySpaced(
                H4("Compétence"),
                Button(
                    "Supprimer",
                    cls=ButtonT.destructive,
                    type="button",
                    onclick="removeItem(this)",
                ),
            ),
            cls="space-y-4",
        ),
        cls="repeatable-item",
    )