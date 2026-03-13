"""Context manager example for temporary resources."""

from __future__ import annotations

from contextlib import contextmanager


@contextmanager
def managed(label: str):
    print(f"open:{label}")
    try:
        yield {"label": label}
    finally:
        print(f"close:{label}")


if __name__ == "__main__":
    with managed("session") as info:
        print(info)
