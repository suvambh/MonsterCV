from __future__ import annotations

from fasthtml.common import *
from monsterui.all import *


def page_scripts() -> Script:
    return Script("""
        function removeItem(btn) {
            const item = btn.closest('.repeatable-item');
            if (!item) return;
            item.remove();
        }

        function previewPhoto(input) {
            const file = input.files && input.files[0];
            const preview = document.getElementById('photo-preview');

            if (!preview) return;

            if (!file) {
                preview.src = '';
                preview.classList.add('hidden');
                return;
            }

            preview.src = URL.createObjectURL(file);
            preview.classList.remove('hidden');
        }
    """)


def text_value(item: dict | None, key: str) -> str:
    return item.get(key, "") if item else ""


def textarea_value(item: dict | None, key: str) -> str:
    values = item.get(key, []) if item else []
    return "\\n".join(values)


def list_to_csv(items: list[str] | None) -> str:
    return ", ".join(items or [])


def message_alert(message: str | None = None, error: bool = False):
    if not message:
        return ""
    return Alert(message, cls=AlertT.error if error else AlertT.success)


def section_header(title: str, subtitle: str | None = None):
    parts = [H3(title)]
    if subtitle:
        parts.append(Subtitle(subtitle))
    return Div(*parts, cls="space-y-1")