from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from cv_schema import empty_cv

def _as_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalize_string_list(value: Any) -> list[str]:
    items = _as_list(value)
    out: list[str] = []

    for item in items:
        if item is None:
            continue
        s = str(item).strip()
        if s:
            out.append(s)

    return out


def _normalize_experience(items: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    for item in _as_list(items):
        if not isinstance(item, dict):
            continue

        out.append(
            {
                "role": _as_str(item.get("role")),
                "company": _as_str(item.get("company")),
                "duration": _as_str(item.get("duration")),
                "location": _as_str(item.get("location")),
                "tech": _as_str(item.get("tech")),
                "details": _normalize_string_list(item.get("details")),
            }
        )

    return out


def _normalize_projects(items: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    for item in _as_list(items):
        if not isinstance(item, dict):
            continue

        out.append(
            {
                "name": _as_str(item.get("name")),
                "tech": _as_str(item.get("tech")),
                "details": _normalize_string_list(item.get("details")),
            }
        )

    return out


def _normalize_education(items: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    for item in _as_list(items):
        if not isinstance(item, dict):
            continue

        out.append(
            {
                "degree": _as_str(item.get("degree")),
                "institution": _as_str(item.get("institution")),
                "location": _as_str(item.get("location")),
                "year": _as_str(item.get("year")),
            }
        )

    return out


def _normalize_certifications(items: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    for item in _as_list(items):
        if not isinstance(item, dict):
            continue

        out.append(
            {
                "name": _as_str(item.get("name")),
                "issuer": _as_str(item.get("issuer")),
                "year": _as_str(item.get("year")),
            }
        )

    return out


def _normalize_skills(items: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    for item in _as_list(items):
        if not isinstance(item, dict):
            continue

        out.append(
            {
                "category": _as_str(item.get("category")),
                "items": _normalize_string_list(item.get("items")),
            }
        )

    return out




def normalize_cv_data(data: dict) -> dict:
    cv = empty_cv()

    cv["name"] = data.get("name", "")
    cv["title"] = data.get("title", "")
    cv["photo"] = data.get("photo", "")
    cv["location"] = data.get("location", "")
    cv["summary"] = data.get("summary", "")

    contact = data.get("contact", {})
    if isinstance(contact, dict):
        cv["contact"]["email"] = contact.get("email", "")
        cv["contact"]["phone"] = contact.get("phone", "")
        cv["contact"]["linkedin"] = contact.get("linkedin", "")
        cv["contact"]["github"] = contact.get("github", "")

    cv["skills"] = data.get("skills", [])
    cv["experience"] = data.get("experience", [])
    cv["projects"] = data.get("projects", [])
    cv["education"] = data.get("education", [])
    cv["certifications"] = data.get("certifications", [])

    return cv


def load_cv_json(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise ValueError("CV JSON root must be an object")

    return normalize_cv_data(raw)


def load_cv_json_from_bytes(content: bytes) -> dict[str, Any]:
    raw = json.loads(content.decode("utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("CV JSON root must be an object")

    return normalize_cv_data(raw)