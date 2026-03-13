"""Stage 07: SQLite connection and transaction example."""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "app.db"


def main() -> None:
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE)"
        )
        cur.execute("INSERT OR IGNORE INTO users(email) VALUES (?)", ("dev@example.com",))
        conn.commit()

        rows = cur.execute("SELECT id, email FROM users ORDER BY id").fetchall()
        print(rows)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
