"""Tests for capstone repository layer."""

from pathlib import Path
import sys


def test_enqueue_and_process_flow(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "capstone.db"
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from app import repository

    monkeypatch.setattr(repository, "DB_FILE", db_path)

    repository.init_db()
    task_id = repository.enqueue_task("sync-inventory")
    assert task_id > 0

    queued = repository.fetch_next_queued()
    assert queued is not None
    assert queued[0] == task_id

    repository.mark_processed(task_id)
    stats = repository.summary()
    assert stats["processed"] == 1
