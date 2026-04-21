from __future__ import annotations

from pathlib import Path

from infrastructure.json_repository import JSONRepository
from infrastructure.pdf_service import PDFService
from infrastructure.render_service import RenderService
from infrastructure.service_adapters import PDFServiceAdapter, RenderServiceAdapter

from use_cases.ensure_cv_preview import EnsureCVPreview
from use_cases.generate_cv_outputs import GenerateCVOutputs


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"


repository = JSONRepository(DATA_DIR / "cv_data.json")
render_service = RenderService(TEMPLATES_DIR, default_theme="terminal.css")
pdf_service = PDFService(BASE_DIR, weasyprint_bin="weasyprint")

renderer = RenderServiceAdapter(render_service)
pdf_generator = PDFServiceAdapter(pdf_service)

generate_cv_outputs = GenerateCVOutputs(
    repository=repository,
    renderer=renderer,
    pdf_generator=pdf_generator,
    output_dir=OUTPUT_DIR,
)

ensure_cv_preview = EnsureCVPreview(
    repository=repository,
    output_generator=generate_cv_outputs,
    output_dir=OUTPUT_DIR,
)