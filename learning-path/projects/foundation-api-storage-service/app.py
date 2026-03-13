"""API + storage milestone starter."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3

DB = "foundation_service.db"


def init_db() -> None:
    conn = sqlite3.connect(DB)
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, event TEXT)")
        conn.execute("INSERT INTO logs(event) VALUES ('service_started')")
        conn.commit()
    finally:
        conn.close()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            body = json.dumps({"status": "ok"}).encode("utf-8")
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    init_db()
    server = HTTPServer(("127.0.0.1", 9100), Handler)
    print("Serving on http://127.0.0.1:9100")
    server.serve_forever()
