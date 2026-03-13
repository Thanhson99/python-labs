"""Typing generics example."""

from typing import TypeVar, Iterable

T = TypeVar("T")


def first(items: Iterable[T]) -> T:
    for item in items:
        return item
    raise ValueError("empty iterable")


if __name__ == "__main__":
    print(first(["a", "b"]))
