"""
Template Renderer for Percipience SaaS Portal
Modularly combines base shell, reusable components, static styles, scripts,
and discrete page section templates.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from workplace.portal.content.manager import content_manager


class TemplateRenderer:
    """Assembles modular HTML pages and assets into complete portal HTML."""

    _PORTAL_DIR = Path(__file__).resolve().parents[1]
    _TEMPLATES_DIR = _PORTAL_DIR / "templates"
    _STATIC_DIR = _PORTAL_DIR / "static"
    _PAGES_ORDER = [
        "overview",
        "platform",
        "comparatives",
        "economics",
        "lab",
        "resources",
        "client_space"
    ]

    _cached_html: Optional[str] = None

    @classmethod
    def render(cls, force_reload: bool = False) -> str:
        """Renders and returns the complete, consolidated PORTAL_HTML string."""
        if cls._cached_html and not force_reload:
            return cls._cached_html

        base_html = (cls._TEMPLATES_DIR / "base.html").read_text(encoding="utf-8")
        header_html = (cls._TEMPLATES_DIR / "components" / "header.html").read_text(encoding="utf-8")
        portal_css = (cls._STATIC_DIR / "css" / "portal.css").read_text(encoding="utf-8")
        head_nav_js = (cls._STATIC_DIR / "js" / "head_nav.js").read_text(encoding="utf-8")
        portal_app_js = (cls._STATIC_DIR / "js" / "portal_app.js").read_text(encoding="utf-8")

        # Assemble page content in deterministic order
        pages_parts = []
        for page_name in cls._PAGES_ORDER:
            page_file = cls._TEMPLATES_DIR / "pages" / f"{page_name}.html"
            if page_file.exists():
                pages_parts.append(page_file.read_text(encoding="utf-8"))

        pages_content = "\n\n".join(pages_parts)

        # Retrieve site metadata from content manager
        meta = content_manager.get_site_meta()
        title = meta.get("page_title", "Percipience | Enterprise Context Engineering OS")

        # Compile final HTML
        html = base_html.replace("{{ page_title }}", title)
        html = html.replace("{{ portal_css }}", portal_css)
        html = html.replace("{{ head_nav_js }}", head_nav_js)
        html = html.replace("{{ header_component }}", header_html)
        html = html.replace("{{ pages_content }}", pages_content)
        html = html.replace("{{ portal_app_js }}", portal_app_js)

        cls._cached_html = html
        return html

    @classmethod
    def render_page(cls, page_name: str) -> str:
        """Returns the isolated HTML fragment for a given page/tab."""
        page_file = cls._TEMPLATES_DIR / "pages" / f"{page_name}.html"
        if not page_file.exists():
            return f"<section id=\"{page_name}\">Page not found</section>"
        return page_file.read_text(encoding="utf-8")

    @classmethod
    def clear_cache(cls) -> None:
        """Invalidates template cache for hot reloads."""
        cls._cached_html = None
        content_manager.reload()
