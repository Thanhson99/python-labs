"""Stage 06: minimal API service using stdlib http.server."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


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

        if self.path.startswith("/users/"):
            user_id = self.path.split("/")[-1]
            self._send({"id": user_id, "name": f"user-{user_id}"})
            return

        self._send({"error": "not found"}, status=404)


def main() -> None:
    server = HTTPServer(("127.0.0.1", 9090), Handler)
    print("Serving on http://127.0.0.1:9090")
    server.serve_forever()


if __name__ == "__main__":
    main()
