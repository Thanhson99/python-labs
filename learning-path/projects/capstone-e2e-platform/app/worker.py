"""Background worker for queued tasks."""

from __future__ import annotations

import time

from repository import fetch_next_queued, mark_processed


def process_task(task_id: int, name: str) -> None:
    print(f"processing task_id={task_id} name={name}")
    time.sleep(0.2)
    mark_processed(task_id)


def run_once() -> bool:
    item = fetch_next_queued()
    if not item:
        print("no queued task")
        return False

    task_id, name = item
    process_task(task_id, name)
    return True


if __name__ == "__main__":
    while run_once():
        pass
