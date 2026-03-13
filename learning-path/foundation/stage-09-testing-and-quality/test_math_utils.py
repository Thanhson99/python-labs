"""Pytest examples for stage 09."""

import pytest

from math_utils import add, normalize_ratio


def test_add() -> None:
    assert add(2, 3) == 5


def test_normalize_ratio() -> None:
    assert normalize_ratio(3.14159) == 3.14


def test_normalize_ratio_invalid() -> None:
    with pytest.raises(ValueError):
        normalize_ratio(-1)
