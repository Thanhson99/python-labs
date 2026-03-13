"""Decorator examples: timing and retry wrapper."""

from __future__ import annotations

import time
from functools import wraps


def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{fn.__name__} took {elapsed:.2f}ms")
        return result

    return wrapper


@timed
def compute(n: int) -> int:
    return sum(i * i for i in range(n))


if __name__ == "__main__":
    print(compute(10000))
