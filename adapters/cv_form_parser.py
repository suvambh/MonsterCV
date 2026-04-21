from __future__ import annotations

from typing import Any

from cv_loader import normalize_cv_data


def _first_value(form: Any, key: str, default: str = "") -> str:
    value = form.get(key, default)
    if value is None:
        return default
    return str(value)


def _list_values(form: Any, key: str) -> list[str]:
    if hasattr(form, "getlist"):
        values = form.getlist(key)
    else:
        value = form.get(key, [])
        if isinstance(value, list):
            values = value
        elif value is None:
            values = []
        else:
            values = [value]

    out: list[str] = []
    for v in values:
        if v is None:
            out.append("")
        else:
            out.append(str(v))
    return out


def _split_csv(value: str) -> list[str]:
    parts = [part.strip() for part in value.split(",")]
    return [part for part in parts if part]


def _strip_or_empty(value: str) -> str:
    return value.strip() if value else ""


def _lines_to_list(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _zip_dicts(*lists: list[str]) -> list[tuple[str, ...]]:
    max_len = max((len(lst) for lst in lists), default=0)
    padded: list[list[str]] = []

    for lst in lists:
        copy = list(lst)
        copy.extend([""] * (max_len - len(copy)))
        padded.append(copy)

    return list(zip(*padded))


def _parse_skills(form: Any) -> list[dict[str, Any]]:
    categories = _list_values(form, "skill_category[]")
    items_values = _list_values(form, "skill_items[]")

    out: list[dict[str, Any]] = []
    for category, items_csv in _zip_dicts(categories, items_values):
        category = _strip_or_empty(category)
        items = _split_csv(items_csv)

        if not category and not items:
            continue

        out.append(
            {
                "category": category,
                "items": items,
            }
        )
    return out


def _parse_experience(form: Any) -> list[dict[str, Any]]:
    roles = _list_values(form, "experience_role[]")
    companies = _list_values(form, "experience_company[]")
    durations = _list_values(form, "experience_duration[]")
    locations = _list_values(form, "experience_location[]")
    techs = _list_values(form, "experience_tech[]")
    details_values = _list_values(form, "experience_details[]")

    out: list[dict[str, Any]] = []
    for role, company, duration, location, tech, details_text in _zip_dicts(
        roles, companies, durations, locations, techs, details_values
    ):
        role = _strip_or_empty(role)
        company = _strip_or_empty(company)
        duration = _strip_or_empty(duration)
        location = _strip_or_empty(location)
        tech = _strip_or_empty(tech)
        details = _lines_to_list(details_text)

        if not any([role, company, duration, location, tech, details]):
            continue

        out.append(
            {
                "role": role,
                "company": company,
                "duration": duration,
                "location": location,
                "tech": tech,
                "details": details,
            }
        )
    return out


def _parse_projects(form: Any) -> list[dict[str, Any]]:
    names = _list_values(form, "project_name[]")
    techs = _list_values(form, "project_tech[]")
    details_values = _list_values(form, "project_details[]")

    out: list[dict[str, Any]] = []
    for name, tech, details_text in _zip_dicts(names, techs, details_values):
        name = _strip_or_empty(name)
        tech = _strip_or_empty(tech)
        details = _lines_to_list(details_text)

        if not any([name, tech, details]):
            continue

        out.append(
            {
                "name": name,
                "tech": tech,
                "details": details,
            }
        )
    return out


def _parse_education(form: Any) -> list[dict[str, Any]]:
    degrees = _list_values(form, "education_degree[]")
    institutions = _list_values(form, "education_institution[]")
    locations = _list_values(form, "education_location[]")
    years = _list_values(form, "education_year[]")

    out: list[dict[str, Any]] = []
    for degree, institution, location, year in _zip_dicts(
        degrees, institutions, locations, years
    ):
        degree = _strip_or_empty(degree)
        institution = _strip_or_empty(institution)
        location = _strip_or_empty(location)
        year = _strip_or_empty(year)

        if not any([degree, institution, location, year]):
            continue

        out.append(
            {
                "degree": degree,
                "institution": institution,
                "location": location,
                "year": year,
            }
        )
    return out


def _parse_certifications(form: Any) -> list[dict[str, Any]]:
    names = _list_values(form, "cert_name[]")
    issuers = _list_values(form, "cert_issuer[]")
    years = _list_values(form, "cert_year[]")

    out: list[dict[str, Any]] = []
    for name, issuer, year in _zip_dicts(names, issuers, years):
        name = _strip_or_empty(name)
        issuer = _strip_or_empty(issuer)
        year = _strip_or_empty(year)

        if not any([name, issuer, year]):
            continue

        out.append(
            {
                "name": name,
                "issuer": issuer,
                "year": year,
            }
        )
    return out


def parse_cv_form_data(form: Any) -> dict[str, Any]:
    raw = {
        "name": _first_value(form, "name"),
        "title": _first_value(form, "title"),
        "photo": _first_value(form, "photo"),
        "location": _first_value(form, "location"),
        "summary": _first_value(form, "summary"),
        "contact": {
            "email": _first_value(form, "contact_email"),
            "phone": _first_value(form, "contact_phone"),
            "linkedin": _first_value(form, "contact_linkedin"),
            "github": _first_value(form, "contact_github"),
        },
        "skills": _parse_skills(form),
        "experience": _parse_experience(form),
        "projects": _parse_projects(form),
        "education": _parse_education(form),
        "certifications": _parse_certifications(form),
    }

    return normalize_cv_data(raw)