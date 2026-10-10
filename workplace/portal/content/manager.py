"""
Portal Content Manager
Handles centralized loading, caching, and querying of structured portal content:
- Site metadata, branding, and navigation
- Pricing tiers, quotas, and limits
- Deep architectural capabilities & SLAs
- Competitive comparison matrices
- Cloud hosting economics & FinOps assumptions
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class PortalContentManager:
    """Centralized content management engine for Percipience Portal."""

    _CONTENT_DIR = Path(__file__).resolve().parent

    def __init__(self, content_dir: Optional[Path] = None):
        self.content_dir = content_dir or self._CONTENT_DIR
        self._cache: Dict[str, Any] = {}

    def _load_json(self, filename: str) -> Dict[str, Any]:
        if filename in self._cache:
            return self._cache[filename]
        file_path = self.content_dir / filename
        if not file_path.exists():
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._cache[filename] = data
                return data
        except Exception:
            return {}

    def get_site_meta(self) -> Dict[str, Any]:
        """Returns application branding, title, and hero metadata."""
        return self._load_json("site_meta.json")

    def get_navigation(self) -> List[Dict[str, Any]]:
        """Returns top navigation items and state."""
        meta = self.get_site_meta()
        return meta.get("navigation", [])

    def get_pricing_tiers(self) -> List[Dict[str, Any]]:
        """Returns commercial tiers specifications and pricing."""
        data = self._load_json("pricing_tiers.json")
        return data.get("tiers", [])

    def get_capabilities(self) -> List[Dict[str, Any]]:
        """Returns 8 deep architectural capabilities and SLAs."""
        data = self._load_json("capabilities.json")
        return data.get("capabilities", [])

    def get_comparative_matrix(self) -> Dict[str, Any]:
        """Returns competitive differentiation breakdown."""
        return self._load_json("comparative_matrix.json")

    def get_economics(self) -> Dict[str, Any]:
        """Returns AWS vs GCP hosting economics and FinOps assumptions."""
        return self._load_json("economics.json")

    def reload(self) -> None:
        """Clears content cache for hot reloading during development."""
        self._cache.clear()


# Default singleton instance
content_manager = PortalContentManager()
