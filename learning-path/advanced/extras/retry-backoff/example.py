"""Retry with exponential backoff."""

import time


def retry_call(fn, retries: int = 4):
    delay = 0.1
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            if attempt == retries:
                raise
            print(f"attempt={attempt} error={exc} wait={delay}")
            time.sleep(delay)
            delay *= 2


if __name__ == "__main__":
    state = {"n": 0}

    def flaky():
        state["n"] += 1
        if state["n"] < 3:
            raise RuntimeError("temporary")
        return "ok"

    print(retry_call(flaky))
