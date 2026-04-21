# Architecture Overview

## 1. Purpose

MonsterCV is a web application for creating, editing, and exporting CVs. The system supports:

* interactive editing via a MonsterUI form
* JSON import/export of CV data
* HTML rendering
* PDF generation

The architecture has been refactored toward a layered structure inspired by Clean Architecture, with a focus on:

* separation of concerns
* explicit data flow
* reduced coupling between layers
* improved readability for both humans and AI systems

---

## 2. Architectural Style

The system follows a **layered architecture with Clean Architecture influences**, organized into:

```
domain/
use_cases/
adapters/
infrastructure/
ui/
routes/
main.py
dependencies.py
```

### Dependency Direction

The intended dependency flow is:

```
routes / UI (outer layer)
        ↓
use_cases (application layer)
        ↓
domain (core data)
```

and

```
use_cases
    ↓
adapters / infrastructure (details)
```

No inner layer should depend on an outer layer.

---

## 3. Layer Responsibilities

### 3.1 Domain Layer (`domain/`)

**Purpose:** Define the canonical CV data structure.

* `cv_schema.py` defines:

  * `empty_cv()`
  * `empty_contact()`

This layer represents the **core data model** of the system.

Current design:

* dictionary-based schema (not class-based entities)
* acts as a single source of truth for CV structure

**Clean Architecture note:**
This corresponds to **Entities**, but currently implemented as structured dictionaries rather than rich domain objects.

---

### 3.2 Use Case Layer (`use_cases/`)

**Purpose:** Implement application-specific behavior.

This layer contains **explicit use cases**, replacing the earlier monolithic service.

#### `cv_persistence.py`

* load CV from repository
* save CV to repository

#### `generate_cv_outputs.py`

* generate HTML via `RenderService`
* generate PDF via `PDFService`
* optionally persist + generate

#### `ensure_cv_preview.py`

* ensure preview files exist
* generate them if missing

#### `editor_workflow_service.py`

* orchestrates the editor save workflow:

  * parse form input
  * preserve existing photo if needed
  * save uploaded photo
  * call output generation
  * return result

**Clean Architecture note:**
This layer corresponds to **Use Cases / Interactors**.
Each file represents a distinct application action.

---

### 3.3 Adapter Layer (`adapters/`)

**Purpose:** Convert external input into canonical domain data.

#### `cv_form_parser.py`

* parses HTTP form data
* converts repeated fields into structured lists
* outputs normalized CV dictionary

#### `cv_loader.py`

* loads CV from JSON
* normalizes into canonical schema

**Key principle:**
All inputs (form, JSON) are normalized into the same structure.

**Clean Architecture note:**
This layer corresponds to **Interface Adapters**.

---

### 3.4 Infrastructure Layer (`infrastructure/`)

**Purpose:** Implement external system interactions.

#### `cv_repository.py`

* JSON-based persistence

#### `render_service.py`

* Jinja-based HTML rendering
* converts `/static/...` paths to file URIs for PDF

#### `pdf_service.py`

* PDF generation via WeasyPrint

#### `upload_service.py`

* file upload handling
* saves files to `static/uploads`
* returns browser-safe paths

**Clean Architecture note:**
This layer corresponds to **Frameworks and Drivers**.

---

### 3.5 UI Layer (`ui/`)

**Purpose:** Build the user interface using MonsterUI.

#### `editor_page.py`

* main page composition
* JSON upload section
* editor form

#### `ui_sections.py`

* reusable form sections
* repeatable blocks (experience, projects, etc.)

#### `ui_cards.py`

* individual card components

#### `ui_helpers.py`

* JS helpers (preview, deletion)
* alert and layout helpers

**Key property:**
UI is declarative and separated from application logic.

---

### 3.6 Route Layer (`routes/`)

**Purpose:** Handle HTTP requests and map them to use cases.

#### `editor_routes.py`

* `/` → render editor page
* `/load-json` → load CV from file
* `/save` → execute save workflow
* HTMX endpoints → dynamic UI fragments

This layer:

* receives requests
* delegates to use cases
* returns UI responses

**Clean Architecture note:**
This is part of the outer interface adapter layer.

---

### 3.7 Composition Root (`dependencies.py`)

**Purpose:** Wire concrete implementations.

Responsibilities:

* instantiate repository, render service, PDF service
* construct use cases
* expose ready-to-use objects

Example:

```python
cv_persistence = CVPersistence(...)
generate_cv_outputs = GenerateCVOutputs(...)
ensure_cv_preview = EnsureCVPreview(...)
```

**Clean Architecture note:**
This is the **composition root**.
It is the only place that knows concrete implementations.

---

### 3.8 Application Entry Point (`main.py`)

**Purpose:** Start the application.

Responsibilities:

* create FastHTML app
* register routes
* start server

Example:

```python
app, rt = fast_app(...)
register_editor_routes(rt)
serve()
```

`main.py` is now intentionally minimal.

---

## 4. Data Flow

### 4.1 Save Flow

```
HTTP POST /save
    ↓
routes.editor_routes
    ↓
EditorWorkflowService
    ↓
parse_cv_form_data (adapter)
    ↓
UploadService (infrastructure)
    ↓
GenerateCVOutputs (use case)
    ↓
RenderService + PDFService (infrastructure)
    ↓
Response (UI)
```

---

### 4.2 JSON Load Flow

```
HTTP POST /load-json
    ↓
routes.editor_routes
    ↓
cv_loader (adapter)
    ↓
normalize_cv_data
    ↓
Update in-memory state
    ↓
Render editor page
```

---

### 4.3 Preview Generation Flow

```
EnsureCVPreview
    ↓
check output files
    ↓
if missing:
    load CV
    generate outputs
```

---

## 5. Key Architectural Decisions

### 5.1 Canonical Data Model

All inputs normalize into a single CV schema.

Benefits:

* consistent rendering
* simpler processing
* fewer edge cases

---

### 5.2 Separation of Concerns

Responsibilities are split across:

* parsing (adapters)
* orchestration (use cases)
* rendering/export (infrastructure)
* UI composition (ui)
* routing (routes)

---

### 5.3 Explicit Use Cases

Application logic is no longer hidden inside a generic service.

Each major operation has a dedicated use case:

* persistence
* output generation
* preview management
* editor workflow

---

### 5.4 Composition Root

All dependencies are constructed in one place (`dependencies.py`).

This:

* centralizes configuration
* prevents hidden coupling
* simplifies future changes

---

### 5.5 Path Invariant for Images

* application state uses `/static/...`
* PDF rendering requires `file:///...`

Conversion is handled **only inside `RenderService`**.

---

## 6. Known Limitations

### 6.1 Domain Model

* currently dictionary-based
* lacks explicit entities/value objects

### 6.2 Global State

* `CURRENT_CV_DATA` is in-memory
* not suitable for multi-user scenarios

### 6.3 Tight Coupling in Use Cases

* use cases depend on concrete infrastructure classes
* no abstract interfaces (ports) yet

### 6.4 UI and Routing Still Coupled via Return Values

* routes return UI components directly
* no separate presenter layer

---

## 7. Future Improvements

* introduce domain entities (CV, Experience, etc.)
* replace global state with session or persistence layer
* introduce interfaces (ports) for repository/render/PDF
* separate presenters/view models from routes
* add tests for use cases independent of UI

---

## 8. Summary

The system has evolved from a flat modular design into a layered architecture with:

* explicit use cases
* clear separation between policy and details
* centralized dependency wiring
* structured data flow

It is not yet a full Clean Architecture implementation, but it follows its core principles and provides a strong foundation for further refinement.
