#!/usr/bin/env python3
"""Serve learning site with interactive example execution API."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT_DIR / "site"
LEARNING_PATH_DIR = ROOT_DIR / "learning-path"


def safe_example_path(relative_path: str) -> Path:
    """Resolve and validate example path inside learning-path."""
    candidate = (ROOT_DIR / relative_path).resolve()
    learning_root = LEARNING_PATH_DIR.resolve()
    if not str(candidate).startswith(str(learning_root)):
        raise ValueError("Path is outside learning-path")
    return candidate


def run_example(example_file: str) -> dict:
    """Run a Python example file and return execution output."""
    path = safe_example_path(example_file)
    if not path.exists() or not path.is_file():
        return {"ok": False, "error": f"Example file not found: {example_file}"}
    if path.suffix != ".py":
        return {"ok": False, "error": "Only .py examples are executable from the web runner."}

    python_cmd = [sys.executable or "python3"]
    cmd = python_cmd + [str(path)]

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(path.parent),
            capture_output=True,
            text=True,
            timeout=15,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "error": "Execution timed out after 15 seconds.",
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
        }

    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "command": " ".join(cmd),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


class LearningHandler(SimpleHTTPRequestHandler):
    """HTTP handler with API endpoints for interactive learning features."""

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._send_json({"status": "ok"}, HTTPStatus.OK)
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/run-example":
            self._handle_run_example()
            return
        self._send_json({"ok": False, "error": "Not found"}, HTTPStatus.NOT_FOUND)

    def _handle_run_example(self) -> None:
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            payload = json.loads(raw_body.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self._send_json({"ok": False, "error": "Invalid JSON payload"}, HTTPStatus.BAD_REQUEST)
            return

        example_file = payload.get("example_file")
        if not example_file or not isinstance(example_file, str):
            self._send_json({"ok": False, "error": "example_file is required"}, HTTPStatus.BAD_REQUEST)
            return

        try:
            result = run_example(example_file)
        except ValueError as exc:
            self._send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return

        status = HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST
        self._send_json(result, status)

    def _send_json(self, data: dict, status: HTTPStatus) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve learning site with interactive API")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--site-dir", default=str(SITE_DIR))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    site_dir = Path(args.site_dir)
    os.chdir(site_dir)

    server = ThreadingHTTPServer((args.host, args.port), LearningHandler)
    print(f"Serving site at http://{args.host}:{args.port}")
    print("Interactive API: POST /api/run-example")
    server.serve_forever()


if __name__ == "__main__":
    main()
