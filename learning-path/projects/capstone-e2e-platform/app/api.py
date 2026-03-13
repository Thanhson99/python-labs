"""HTTP API for task ingestion."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from repository import init_db, enqueue_task, summary


class Handler(BaseHTTPRequestHandler):
    def _send(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send({"status": "ok"})
            return
        if self.path == "/metrics":
            self._send(summary())
            return
        self._send({"error": "not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/tasks":
            self._send({"error": "not found"}, status=404)
            return

        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        name = str(payload.get("name", "")).strip()
        if not name:
            self._send({"error": "name is required"}, status=400)
            return

        task_id = enqueue_task(name)
        self._send({"task_id": task_id, "status": "queued"}, status=201)


def main() -> None:
    init_db()
    server = HTTPServer(("127.0.0.1", 9200), Handler)
    print("API listening on http://127.0.0.1:9200")
    server.serve_forever()


if __name__ == "__main__":
    main()
