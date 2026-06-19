import json
import os
import threading
import time
from datetime import datetime, timezone
from contextlib import contextmanager
from email.message import Message
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from io import BytesIO
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from . import generate_recovery_plan, get_incident_definition, get_incident_questionnaire, list_supported_incidents
from .report import render_markdown
from .validation import ValidationError, validate_situation


FEEDBACK_EVENTS: list[dict[str, Any]] = []
FEEDBACK_MAX_EVENTS = 100
RATE_LIMIT_EVENTS: dict[str, list[float]] = {}
RATE_LIMIT_MAX_REQUESTS = int(os.environ.get("ARA_RATE_LIMIT_MAX_REQUESTS", "120"))
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("ARA_RATE_LIMIT_WINDOW_SECONDS", "60"))
ALLOWED_FEEDBACK_OUTCOMES = {"recovered", "stuck"}
ALLOWED_LINK_FEEDBACK = {"worked", "failed", "not_used"}


def _static_dir() -> Path:
    return Path(str(files("account_recovery_assistant").joinpath("static")))


def _html_shell() -> str:
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Account Recovery Wizard</title>
    <link rel="stylesheet" href="/static/app.css">
  </head>
  <body>
    <main id="app">
      <header class="hero">
        <p class="eyebrow">Safety-first recovery</p>
        <h1>Account Recovery Wizard</h1>
        <p class="lede">Choose a real incident, answer a short questionnaire, and get a recovery plan that uses official channels only.</p>
      </header>
      <section class="panel">
        <div id="status">Loading incidents...</div>
        <div id="wizard"></div>
      </section>
    </main>
    <script src="/static/app.js"></script>
  </body>
</html>
"""


def _json_response(handler: BaseHTTPRequestHandler, payload: dict[str, Any], status: int = 200) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _text_response(
    handler: BaseHTTPRequestHandler,
    body: str,
    content_type: str = "text/html; charset=utf-8",
    status: int = HTTPStatus.OK,
) -> None:
    data = body.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _asset_response(handler: BaseHTTPRequestHandler, name: str, content_type: str) -> None:
    path = _static_dir() / name
    data = path.read_bytes()
    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)



def _rate_limit_key(handler: BaseHTTPRequestHandler) -> str:
    client_address = getattr(handler, "client_address", ("local", 0))
    return str(client_address[0])


def _rate_limit_allows(handler: BaseHTTPRequestHandler) -> bool:
    now = time.monotonic()
    key = _rate_limit_key(handler)
    window_start = now - RATE_LIMIT_WINDOW_SECONDS
    events = [event for event in RATE_LIMIT_EVENTS.get(key, []) if event >= window_start]
    if len(events) >= RATE_LIMIT_MAX_REQUESTS:
        RATE_LIMIT_EVENTS[key] = events
        return False
    events.append(now)
    RATE_LIMIT_EVENTS[key] = events
    return True


def _rate_limit_response(handler: BaseHTTPRequestHandler) -> None:
    _json_response(
        handler,
        {
            "error": "Rate limit exceeded",
            "detail": "Too many requests in a short period. Please wait and try again.",
        },
        status=429,
    )



def _handle_feedback(handler: BaseHTTPRequestHandler, payload: dict[str, Any]) -> None:
    if payload.get("consent") is not True:
        _json_response(
            handler,
            {"error": "Consent required", "detail": "Feedback is only accepted when consent is true."},
            status=400,
        )
        return

    outcome = str(payload.get("outcome", "")).lower()
    link_status = str(payload.get("link_status", "not_used")).lower()
    if outcome not in ALLOWED_FEEDBACK_OUTCOMES:
        _json_response(handler, {"error": "Validation error", "field": "outcome", "detail": "Unsupported outcome."}, status=400)
        return
    if link_status not in ALLOWED_LINK_FEEDBACK:
        _json_response(
            handler,
            {"error": "Validation error", "field": "link_status", "detail": "Unsupported link feedback."},
            status=400,
        )
        return

    FEEDBACK_EVENTS.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "consent": True,
            "incident_id": payload.get("incident_id"),
            "decision_path_id": payload.get("decision_path_id"),
            "outcome": outcome,
            "link_status": link_status,
        }
    )
    if len(FEEDBACK_EVENTS) > FEEDBACK_MAX_EVENTS:
        del FEEDBACK_EVENTS[: len(FEEDBACK_EVENTS) - FEEDBACK_MAX_EVENTS]
    _json_response(
        handler,
        {"accepted": True, "stored": "memory_only", "count": len(FEEDBACK_EVENTS), "max_events": FEEDBACK_MAX_EVENTS},
    )


class _WizardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        try:
            if self.path == "/":
                _text_response(self, _html_shell())
                return
            if self.path == "/static/app.css":
                _asset_response(self, "app.css", "text/css; charset=utf-8")
                return
            if self.path == "/static/app.js":
                _asset_response(self, "app.js", "application/javascript; charset=utf-8")
                return
            if self.path == "/healthz":
                _json_response(
                    self,
                    {
                        "status": "ok",
                        "incidents": len(list_supported_incidents()),
                        "feedback_events": len(FEEDBACK_EVENTS),
                        "rate_limit_max_requests": RATE_LIMIT_MAX_REQUESTS,
                    },
                )
                return
            if self.path == "/api/incidents":
                _json_response(self, {"incidents": list_supported_incidents()})
                return
            if self.path.startswith("/api/incidents/") and self.path.endswith("/questionnaire"):
                incident_id = self.path[len("/api/incidents/") : -len("/questionnaire")].strip("/")
                incident = get_incident_definition(incident_id)
                _json_response(
                    self,
                    {
                        "incident_id": incident["id"],
                        "service": incident["service"],
                        "title": incident["title"],
                        "questions": get_incident_questionnaire(incident_id),
                    },
                )
                return
            _json_response(self, {"error": "Not found"}, status=404)
        except KeyError as exc:
            _json_response(self, {"error": "Unknown incident", "detail": str(exc)}, status=404)

    def do_POST(self) -> None:
        try:
            if self.path not in {"/api/plan", "/api/plan/markdown", "/api/feedback"}:
                _json_response(self, {"error": "Not found"}, status=404)
                return

            if not _rate_limit_allows(self):
                _rate_limit_response(self)
                return

            content_length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            if not isinstance(payload, dict):
                _json_response(self, {"error": "Validation error", "detail": "Request body must be a JSON object."}, status=400)
                return

            if self.path == "/api/plan":
                validate_situation(payload)
                plan = generate_recovery_plan(payload)
                _json_response(self, plan)
                return

            if self.path == "/api/plan/markdown":
                validate_situation(payload)
                plan = generate_recovery_plan(payload)
                _text_response(self, render_markdown(plan), content_type="text/markdown; charset=utf-8")
                return

            if self.path == "/api/feedback":
                _handle_feedback(self, payload)
                return
        except JSONDecodeError:
            _json_response(self, {"error": "Invalid JSON", "detail": "Request body must be valid JSON."}, status=400)
        except ValidationError as exc:
            _json_response(self, {"error": "Validation error", "field": exc.field, "detail": exc.message}, status=400)
        except KeyError as exc:
            _json_response(self, {"error": "Unknown incident", "detail": str(exc)}, status=404)

    def log_message(self, format: str, *args: object) -> None:
        # No request bodies are logged. Enable basic access logs only for local debugging.
        if os.environ.get("ARA_ACCESS_LOG") == "1":
            super().log_message(format, *args)


class _DispatcherHandler(_WizardHandler):
    def __init__(self, method: str, path: str, body: bytes = b"", headers: dict[str, str] | None = None):
        self.command = method
        self.path = path
        self.client_address = ("127.0.0.1", 0)
        self.rfile = BytesIO(body)
        self.wfile = BytesIO()
        self.headers = Message()
        for key, value in (headers or {}).items():
            self.headers[key] = value
        if body and "Content-Length" not in self.headers:
            self.headers["Content-Length"] = str(len(body))
        self.status_code = 200
        self.response_headers: dict[str, str] = {}

    def send_response(self, code: int, message: str | None = None) -> None:
        self.status_code = code

    def send_header(self, keyword: str, value: str) -> None:
        self.response_headers[keyword] = value

    def end_headers(self) -> None:
        return


def make_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), _WizardHandler)


def dispatch_request(
    method: str,
    path: str,
    body: bytes = b"",
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    handler = _DispatcherHandler(method=method, path=path, body=body, headers=headers)
    if method == "GET":
        handler.do_GET()
    elif method == "POST":
        handler.do_POST()
    else:
        raise ValueError(f"Unsupported method: {method}")
    return {
        "status": handler.status_code,
        "headers": handler.response_headers,
        "body": handler.wfile.getvalue(),
    }


@contextmanager
def run_server_in_thread(host: str = "127.0.0.1", port: int = 0):
    server = make_server(host=host, port=port)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{host}:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = make_server(host=host, port=port)
    print(f"Account Recovery Wizard running at http://{host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
