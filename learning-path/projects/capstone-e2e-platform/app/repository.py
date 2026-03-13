"""Persistence layer for capstone e2e project."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "capstone.db"


def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              status TEXT NOT NULL DEFAULT 'queued',
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              processed_at TEXT
            )
            """
        )


def enqueue_task(name: str) -> int:
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO tasks(name, status) VALUES (?, 'queued')", (name,))
        return int(cur.lastrowid)


def fetch_next_queued() -> tuple[int, str] | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, name FROM tasks WHERE status='queued' ORDER BY id LIMIT 1"
        ).fetchone()
        return tuple(row) if row else None


def mark_processed(task_id: int) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE tasks SET status='processed', processed_at=CURRENT_TIMESTAMP WHERE id=?",
            (task_id,),
        )


def summary() -> dict:
    with get_conn() as conn:
        queued = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='queued'").fetchone()[0]
        processed = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='processed'").fetchone()[0]
        return {"queued": queued, "processed": processed}


if __name__ == "__main__":
    init_db()
    print(f"initialized: {DB_FILE}")
