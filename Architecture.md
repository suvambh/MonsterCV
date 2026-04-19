# MonsterCV Architecture

## Overview

MonsterCV is a FastHTML + MonsterUI application for building, editing, and exporting CVs.

The system is designed around a **single canonical CV data structure**.
All inputs (form submissions, uploaded JSON) are normalized into this structure before being rendered or exported.

---

## Core Principles

1. **Single Source of Truth**

   * All CV data must conform to the canonical schema.
   * No module should define its own CV structure.

2. **Separation of Concerns**

   * UI → rendering and layout only
   * Parser/Loader → input normalization
   * Services → orchestration
   * Repository → persistence
   * Render/PDF → output generation

3. **Deterministic Flow**

   * Same input → same normalized data → same output

4. **Path Separation Rule**

   * Browser paths and file system paths must never be mixed.

---

## Canonical CV Schema

All data must normalize into the following structure:

```python
{
  "name": str,
  "title": str,
  "photo": str,
  "location": str,
  "summary": str,
  "contact": {
      "email": str,
      "phone": str,
      "linkedin": str,
      "github": str
  },
  "skills": [{"category": str, "items": [str]}],
  "experience": [...],
  "projects": [...],
  "education": [...],
  "certifications": [...]
}
```

### Notes

* Lists (`experience`, `projects`, etc.) are always arrays (never `None`)
* Missing fields must be filled with defaults during normalization
* Template rendering depends on this exact shape

---

## System Flow

### Editor Flow

1. User edits CV in MonsterUI form
2. Form is submitted to `/save`
3. Photo (if uploaded) is saved to `static/uploads/`
4. Form data is parsed into raw structure
5. Raw data is normalized into canonical schema
6. Data is saved via repository
7. HTML is rendered via template
8. PDF is generated from HTML

---

## Module Responsibilities

### Entry Point

**`main.py`**

* App initialization
* Route definitions
* Connects UI with services
* Should remain thin (no business logic)

---

### UI Layer

**`ui_sections.py`**

* Form sections (personal info, education, etc.)

**`ui_cards.py`**

* Repeatable item components (experience, projects, etc.)

**`ui_helpers.py`**

* Shared UI utilities (labels, alerts, layout helpers)

---

### Input Layer

**`cv_form_parser.py`**

* Converts form data → raw CV structure

**`cv_loader.py`**

* Converts uploaded JSON → normalized CV structure

---

### Domain Layer

**`cv_schema.py` (to be added)**

* Defines canonical CV defaults
* Provides `empty_cv()` and helpers

---

### Service Layer

**`cv_service.py`**

* High-level orchestration:

  * save data
  * trigger render
  * trigger PDF generation

**`cv_services.py`**

* Dependency wiring / service instantiation

---

### Persistence Layer

**`cv_repository.py`**

* Saves and loads CV data (JSON)

---

### Output Layer

**`render_service.py`**

* Renders Jinja template (`templates/cv.html`)
* Converts browser paths → file paths for PDF

**`pdf_service.py`**

* Generates PDF using WeasyPrint

---

## Photo Handling Rules

### In Application State

```text
/static/uploads/file.jpg
```

### In PDF Rendering

```text
file:///absolute/path/to/static/uploads/file.jpg
```

### Important

* Never store `file:///` paths in CV data
* Conversion must happen only in `render_service.py`

---

## Invariants

The following must always hold:

* All data conforms to canonical CV schema
* UI, JSON, and parser all produce the same structure
* Template matches schema exactly
* Photo paths:

  * browser-safe in state
  * filesystem-safe in PDF layer
* No business logic inside UI modules
* No rendering logic inside parser/loader

---

## Current Architecture State

* MonsterUI form editing: working
* JSON upload: working
* Photo upload + preview: working
* HTML rendering: working
* PDF generation: working

The architecture is modular but still evolving.

---

## Future Improvements (Planned Refactors)

* Extract photo upload into dedicated service
* Move save workflow fully into service layer
* Introduce typed CV schema (dataclass or Pydantic)
* Split UI helpers into smaller modules
* Introduce package structure (`services/`, `ui/`, `domain/`, etc.)

---

## Developer Guide

### Where to Make Changes

| Task                       | File                |
| -------------------------- | ------------------- |
| Change form layout         | `ui_sections.py`    |
| Change repeatable UI       | `ui_cards.py`       |
| Change parsing logic       | `cv_form_parser.py` |
| Change JSON input handling | `cv_loader.py`      |
| Change persistence         | `cv_repository.py`  |
| Change render logic        | `render_service.py` |
| Change PDF output          | `pdf_service.py`    |
| Change workflow            | `cv_service.py`     |
| Change routes              | `main.py`           |

---

## Summary

The system is built around a **normalized data pipeline**:

```text
Form / JSON → Parser / Loader → Canonical CV → Service → Render → PDF
```

Maintaining this pipeline cleanly is the key to keeping the codebase scalable and understandable.
