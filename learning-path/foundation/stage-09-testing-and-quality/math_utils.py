"""Stage 09: deterministic utility functions for tests."""


def add(a: int, b: int) -> int:
    return a + b


def normalize_ratio(value: float) -> float:
    if value < 0:
        raise ValueError("value must be non-negative")
    return round(value, 2)
