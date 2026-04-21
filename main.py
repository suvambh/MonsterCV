from __future__ import annotations

from fasthtml.common import *
from monsterui.all import *

from routes.editor_routes import register_editor_routes


app, rt = fast_app(hdrs=Theme.blue.headers())

register_editor_routes(rt)

serve()