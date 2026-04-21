# MonsterCV Architecture (v2)

## 1. Overview

MonsterCV is a CV builder web application built using FastHTML and MonsterUI. The system supports:

* interactive CV editing via a web form
* JSON import/export
* HTML rendering
* PDF generation via WeasyPrint

The architecture follows a **layered design inspired by Clean Architecture**, with an emphasis on:

* clear separation of concerns
* explicit data flow
* reduced coupling between layers
* replaceable infrastructure components

---

## 2. Key Evolution from v1 → v2

### 2.1 Introduction of Ports (Primary Change)

In v1:

* Use cases directly depended on concrete infrastructure classes (`RenderService`, `PDFService`, etc.)
* This caused tight coupling between application logic and implementation details

In v2:

* Use cases depend on **ports (Protocols)** instead of concrete classes
* Infrastructure implements these ports (directly or via adapters)

Result:

* dependency direction is now correct
* application layer is independent of infrastructure

---

### 2.2 Introduction of Adapters

In v1:

* Infrastructure APIs were used directly inside use cases

In v2:

* **Adapters translate infrastructure APIs into port-compatible interfaces**

Examples:

* `RenderServiceAdapter` → exposes `render(...)`
* `PDFServiceAdapter` → exposes `generate(...)`

Result:

* infrastructure can evolve independently
* use cases remain stable

---

### 2.3 Removal / Simplification of Intermediate Services

* `CVPersistence` is now redundant or minimized
* Use cases interact directly with `CVRepositoryPort`

Result:

* fewer unnecessary abstraction layers
* clearer ownership of responsibilities

---

### 2.4 Stronger Composition Root

`dependencies.py` now fully acts as a **composition root**:

* constructs concrete implementations
* wraps them in adapters when necessary
* injects them into use cases

Result:

* all wiring is centralized
* no hidden instantiation logic

---

## 3. Architectural Layers

```
domain/
use_cases/
adapters/
infrastructure/
ui/
routes/
dependencies.py
main.py
```

### Dependency Direction

```
routes / UI
        ↓
use_cases (depends on ports)
        ↓
domain

use_cases
        ↓
ports (interfaces)
        ↓
infrastructure (via adapters)
```

No use case depends directly on infrastructure.

---

## 4. Ports and Adapters

### 4.1 Ports (Application Boundary)

Defined in:

```
use_cases/ports.py
```

Ports describe **capabilities required by use cases**.

Example:

```python
class CVRepositoryPort(Protocol):
    def load(self) -> CVData: ...
    def save(self, data: CVData) -> None: ...
```

Other ports:

* `CVRendererPort`
* `PDFGeneratorPort`
* `PhotoStoragePort`
* `CVOutputGeneratorPort`
* `CVFormParserPort`

Key idea:

> Ports define *what is needed*, not *how it is implemented*

---

### 4.2 Adapters (Infrastructure Translation)

Adapters live in the infrastructure layer and translate real services into port-compatible interfaces.

Example:

```python
class RenderServiceAdapter:
    def render(self, data):
        return self.render_service.render_cv_html(data)
```

```python
class PDFServiceAdapter:
    def generate(self, html_file, pdf_file):
        return self.pdf_service.generate_pdf(html_file, pdf_file)
```

Key idea:

> Adapters bridge mismatches between infrastructure APIs and application expectations

---

### 4.3 Structural Typing

Concrete classes do **not** need to inherit from ports.

Example:

```python
class JSONRepository:
    def load(...): ...
    def save(...): ...
```

This automatically satisfies `CVRepositoryPort`.

---

## 5. Layer Responsibilities (Updated)

### 5.1 Domain Layer (`domain/`)

* defines canonical CV schema
* provides `empty_cv()`

Still:

* dictionary-based (not yet rich entities)

---

### 5.2 Use Case Layer (`use_cases/`)

Implements application workflows using ports.

#### Key Use Cases

##### `GenerateCVOutputs`

* saves CV data
* renders HTML
* writes HTML file
* generates PDF

Dependencies:

* `CVRepositoryPort`
* `CVRendererPort`
* `PDFGeneratorPort`

---

##### `EnsureCVPreview`

* checks if preview files exist
* generates them if missing

Dependencies:

* `CVRepositoryPort`
* `CVOutputGeneratorPort`

---

##### `EditorWorkflowService`

* parses form input
* handles photo upload
* merges state
* triggers output generation

Dependencies:

* `PhotoStoragePort`
* `CVOutputGeneratorPort`
* `CVFormParserPort`

---

### 5.3 Adapter Layer (`adapters/`)

* converts external input into canonical CV data

Examples:

* `cv_form_parser.py`
* `cv_loader.py`

---

### 5.4 Infrastructure Layer (`infrastructure/`)

Implements external systems:

* `JSONRepository` → persistence
* `RenderService` → Jinja rendering
* `PDFService` → WeasyPrint integration
* `UploadService` → file storage

Adapters also live here.

---

### 5.5 UI Layer (`ui/`)

* MonsterUI components
* page composition
* form sections

---

### 5.6 Route Layer (`routes/`)

* receives HTTP requests
* calls use cases
* returns UI

Remains thin.

---

### 5.7 Composition Root (`dependencies.py`)

Responsible for:

* creating concrete services
* wrapping adapters
* injecting dependencies into use cases

Example:

```python
renderer = RenderServiceAdapter(render_service)
pdf_generator = PDFServiceAdapter(pdf_service)

generate_cv_outputs = GenerateCVOutputs(
    repository=repository,
    renderer=renderer,
    pdf_generator=pdf_generator,
    output_dir=OUTPUT_DIR,
)
```

---

## 6. Data Flow (Updated)

### Save Flow

```
HTTP POST /save
    ↓
routes
    ↓
EditorWorkflowService
    ↓
CVFormParserPort
    ↓
PhotoStoragePort
    ↓
GenerateCVOutputs
    ↓
CVRendererPort → HTML
    ↓
PDFGeneratorPort → PDF
```

---

### Preview Flow

```
EnsureCVPreview
    ↓
check files
    ↓
if missing:
    repository.load()
    ↓
    GenerateCVOutputs.generate_outputs()
```

---

## 7. Key Architectural Decisions

### 7.1 Ports Over Concrete Dependencies

Use cases depend only on ports.

Benefits:

* decoupling
* testability
* replaceable infrastructure

---

### 7.2 Adapters for Compatibility

Adapters isolate infrastructure API differences.

Benefits:

* avoids modifying working infrastructure code
* keeps use-case interface clean

---

### 7.3 Canonical Data Model

All inputs normalize to a single CV schema.

Benefits:

* consistent processing
* simplified rendering logic

---

### 7.4 Composition Root

All wiring centralized in `dependencies.py`.

Benefits:

* no hidden instantiation
* easier system modification

---

## 8. Current Limitations (v2)

Still present:

* domain model is dict-based (no entities/value objects)
* global in-memory state exists
* no presenter layer (routes return UI directly)

These were already identified in v1 and remain future work. 

---

## 9. Summary

v2 represents a significant architectural improvement over v1:

* use cases are now independent of infrastructure
* ports define clear application boundaries
* adapters isolate implementation differences
* dependency wiring is centralized

The system now aligns much more closely with Clean Architecture principles while remaining simple and incremental.

