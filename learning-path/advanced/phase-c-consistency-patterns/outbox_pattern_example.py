"""Phase C: outbox pattern with SQLite transaction."""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "outbox.db"


def setup(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, status TEXT NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT, payload TEXT)"
    )


def create_order_with_event(conn: sqlite3.Connection, order_id: str) -> None:
    with conn:
        conn.execute("INSERT OR REPLACE INTO orders(id, status) VALUES (?, ?)", (order_id, "created"))
        conn.execute(
            "INSERT INTO outbox(event_type, payload) VALUES (?, ?)",
            ("order_created", f'{{"order_id":"{order_id}"}}'),
        )


def main() -> None:
    conn = sqlite3.connect(DB)
    setup(conn)
    create_order_with_event(conn, "order-2001")

    outbox_rows = conn.execute("SELECT id, event_type, payload FROM outbox").fetchall()
    print(outbox_rows)
    conn.close()


if __name__ == "__main__":
    main()
