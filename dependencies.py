from __future__ import annotations

from pathlib import Path

from infrastructure.cv_repository import CVRepository
from infrastructure.pdf_service import PDFService
from infrastructure.render_service import RenderService

from use_cases.cv_persistence import CVPersistence
from use_cases.generate_cv_outputs import GenerateCVOutputs
from use_cases.ensure_cv_preview import EnsureCVPreview


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"


repository = CVRepository(DATA_DIR / "cv_data.json")
render_service = RenderService(TEMPLATES_DIR, default_theme="terminal.css")
pdf_service = PDFService(BASE_DIR, weasyprint_bin="weasyprint")

cv_persistence = CVPersistence(repository=repository)

generate_cv_outputs = GenerateCVOutputs(
    persistence=cv_persistence,
    render_service=render_service,
    pdf_service=pdf_service,
    output_dir=OUTPUT_DIR,
    default_theme="terminal.css",
)

ensure_cv_preview = EnsureCVPreview(
    persistence=cv_persistence,
    output_generator=generate_cv_outputs,
    output_dir=OUTPUT_DIR,
)