from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


class RenderService:
    """Render CV data into HTML using Jinja templates."""

    def __init__(self, templates_dir: Path, default_theme: str = "style.css") -> None:
        self.templates_dir = templates_dir
        self.default_theme = default_theme
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

    def _prepare_template_data(self, data: dict[str, Any]) -> dict[str, Any]:
        prepared = dict(data)

        photo = prepared.get("photo", "")
        if isinstance(photo, str) and photo.startswith("/static/"):
            project_root = self.templates_dir.parent
            absolute_photo = (project_root / photo.lstrip("/")).resolve()
            prepared["photo"] = absolute_photo.as_uri()

        return prepared

    def render_cv_html(
        self,
        data: dict[str, Any],
        theme_css: str | None = None,
        template_name: str = "cv.html",
    ) -> str:
        """Render the CV template into an HTML string."""
        theme = theme_css or self.default_theme
        template = self.env.get_template(template_name)
        prepared_data = self._prepare_template_data(data)
        return template.render(**prepared_data, theme_css=theme)

    def save_html(
        self,
        html_content: str,
        output_file: Path,
    ) -> Path:
        """Write rendered HTML to disk."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding="utf-8")
        return output_file

    def render_and_save(
        self,
        data: dict[str, Any],
        output_file: Path,
        theme_css: str | None = None,
        template_name: str = "cv.html",
    ) -> Path:
        """Render CV HTML and save it to disk."""
        html_content = self.render_cv_html(
            data=data,
            theme_css=theme_css,
            template_name=template_name,
        )
        return self.save_html(html_content, output_file)