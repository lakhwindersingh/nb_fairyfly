#!/usr/bin/env python3
"""
Neutron Binary Percipience - Enterprise Product Site & Cloud SaaS Portal
Modular architecture with:
- Dedicated templates and page component managers
- Externalized stylesheets and client scripts
- Centralized content management (specs, SLAs, pricing, capabilities)
- Asynchronous ASGI 3.0 runner (Uvicorn) & native HTTPServer runner
"""

from typing import Optional
import sys
import os
from pathlib import Path
from http.server import HTTPServer

REPO_ROOT = Path(__file__).resolve().parents[2]
for p_dir in [REPO_ROOT, REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    p_str = str(p_dir)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

from workplace.portal.content.manager import content_manager, PortalContentManager
from workplace.portal.templates.renderer import TemplateRenderer
from workplace.portal.core.state import CLIENT_SESSIONS, DEMO_CLIENT
from workplace.portal.core.request_handler import PortalRequestHandler
from workplace.portal.core.asgi_adapter import app

# Render modular portal HTML
PORTAL_HTML = TemplateRenderer.render()


def run_server(port: Optional[int] = None, host: Optional[str] = None):
    try:
        from core.config_manager import config
    except (ImportError, ModuleNotFoundError):
        config = None
    target_port = port or (config.get_int("portal.port", 3000) if config else int(os.environ.get("PORTAL_PORT", "3000")))
    bind_host = host or (config.get_str("portal.host", "0.0.0.0") if config else os.environ.get("PORTAL_HOST", "0.0.0.0"))
    server_address = (bind_host, target_port)
    httpd = HTTPServer(server_address, PortalRequestHandler)
    print(f"🌍 Percipience Cloud SaaS Portal running at http://localhost:{target_port}/ (bound to {bind_host}:{target_port})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down portal server.")
        httpd.server_close()


if __name__ == "__main__":
    cli_port = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_server(cli_port)
