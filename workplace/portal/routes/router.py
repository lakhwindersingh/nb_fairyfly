"""
Central API Route Dispatcher for Percipience Portal.
Allows registration of modular GET, POST, and DELETE endpoint handlers.
"""

from typing import Callable, Dict, Optional, Tuple, Any
from urllib.parse import ParseResult


class APIRouter:
    """Registry and dispatcher for API route handlers."""

    def __init__(self):
        self._get_routes: Dict[str, Callable] = {}
        self._post_routes: Dict[str, Callable] = {}
        self._delete_routes: Dict[str, Callable] = {}

    def get(self, path: str):
        def decorator(handler: Callable):
            self._get_routes[path] = handler
            return handler
        return decorator

    def post(self, path: str):
        def decorator(handler: Callable):
            self._post_routes[path] = handler
            return handler
        return decorator

    def delete(self, path: str):
        def decorator(handler: Callable):
            self._delete_routes[path] = handler
            return handler
        return decorator

    def dispatch_get(self, handler_instance, parsed: ParseResult) -> bool:
        func = self._get_routes.get(parsed.path)
        if func:
            func(handler_instance, parsed)
            return True
        return False

    def dispatch_post(self, handler_instance, parsed: ParseResult) -> bool:
        func = self._post_routes.get(parsed.path)
        if func:
            func(handler_instance, parsed)
            return True
        return False

    def dispatch_delete(self, handler_instance, parsed: ParseResult) -> bool:
        func = self._delete_routes.get(parsed.path)
        if func:
            func(handler_instance, parsed)
            return True
        return False


api_router = APIRouter()
