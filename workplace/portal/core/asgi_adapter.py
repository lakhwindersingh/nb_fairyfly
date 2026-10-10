"""
ASGI Application Adapter for Uvicorn and ASGI 3.0 runtimes.
Bridges asynchronous HTTP requests to PortalRequestHandler with threadpool execution.
"""

import io
import json
import asyncio
from typing import Optional, Any
from email.message import Message
from workplace.portal.core.request_handler import PortalRequestHandler


class _ASGIResponseCollector:
    """Collects HTTP status, headers, and body chunks from PortalRequestHandler."""

    def __init__(self):
        self.status = 200
        self.headers = []
        self.body = bytearray()

    def send_response(self, code: int, message: Optional[str] = None):
        self.status = int(code)

    def send_header(self, keyword: str, value: Any):
        self.headers.append((keyword.lower().encode("latin1"), str(value).encode("latin1")))

    def end_headers(self):
        pass

    def write(self, data: bytes):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.body.extend(data)

    def flush(self):
        pass


def _handle_portal_sync_request(method: str, path: str, headers_list: list, body_bytes: bytes) -> _ASGIResponseCollector:
    """Dispatches a single HTTP request through PortalRequestHandler synchronously."""
    handler = PortalRequestHandler.__new__(PortalRequestHandler)
    handler.path = path
    handler.command = method
    headers = Message()
    for k, v in headers_list:
        headers[k.decode("latin1")] = v.decode("latin1")
    handler.headers = headers
    handler.rfile = io.BytesIO(body_bytes)
    collector = _ASGIResponseCollector()
    handler.send_response = collector.send_response
    handler.send_header = collector.send_header
    handler.end_headers = collector.end_headers
    handler.wfile = collector

    try:
        if method == "GET":
            handler.do_GET()
        elif method == "POST":
            handler.do_POST()
        elif method == "DELETE":
            handler.do_DELETE()
        elif method == "OPTIONS":
            collector.send_response(200)
            collector.send_header("Access-Control-Allow-Origin", "*")
            collector.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
            collector.send_header("Access-Control-Allow-Headers", "*")
            collector.end_headers()
        else:
            collector.send_response(405)
            collector.send_header("Content-Type", "text/plain")
            collector.end_headers()
            collector.write(b"Method Not Allowed")
    except Exception as exc:
        collector.send_response(500)
        collector.send_header("Content-Type", "application/json")
        collector.end_headers()
        collector.write(json.dumps({"error": "Internal Server Error", "detail": str(exc)}).encode("utf-8"))

    return collector


async def app(scope, receive, send):
    """ASGI 3.0 compatible application entrypoint for Uvicorn."""
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return

    if scope["type"] != "http":
        return

    method = scope.get("method", "GET")
    raw_path = scope.get("raw_path")
    if raw_path:
        path = raw_path.decode("latin1")
    else:
        path = scope.get("path", "/")
    query_string = scope.get("query_string", b"").decode("latin1")
    full_path = f"{path}?{query_string}" if query_string else path

    body = bytearray()
    while True:
        message = await receive()
        body.extend(message.get("body", b""))
        if not message.get("more_body", False):
            break

    loop = asyncio.get_running_loop()
    collector = await loop.run_in_executor(
        None,
        _handle_portal_sync_request,
        method,
        full_path,
        scope.get("headers", []),
        bytes(body)
    )

    await send({
        "type": "http.response.start",
        "status": collector.status,
        "headers": collector.headers,
    })
    await send({
        "type": "http.response.body",
        "body": bytes(collector.body),
    })
