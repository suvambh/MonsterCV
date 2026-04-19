from __future__ import annotations

from pathlib import Path

from cv_repository import CVRepository
from cv_service import CVService
from pdf_service import PDFService
from render_service import RenderService


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"


repository = CVRepository(DATA_DIR / "cv_data.json")
render_service = RenderService(TEMPLATES_DIR, default_theme="terminal.css")
pdf_service = PDFService(BASE_DIR, weasyprint_bin="weasyprint")

cv_service = CVService(
    repository=repository,
    render_service=render_service,
    pdf_service=pdf_service,
    output_dir=OUTPUT_DIR,
    default_theme="terminal.css",
)