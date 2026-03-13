"""Tests for distributed patterns examples."""

from pathlib import Path
import importlib.util


def load_module(file_path: Path):
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_idempotency_store_returns_same_result() -> None:
    mod = load_module(Path(__file__).resolve().parents[1] / "idempotency-middleware" / "example.py")
    store = mod.IdempotencyStore()
    state = {"n": 0}

    def op():
        state["n"] += 1
        return state["n"]

    assert store.handle("k", op) == 1
    assert store.handle("k", op) == 1


def test_contract_validation() -> None:
    mod = load_module(Path(__file__).resolve().parents[1] / "contract-testing" / "example.py")
    assert mod.validate_contract({"id": "1", "email": "e@x.com", "status": "ok"}) is True
    assert mod.validate_contract({"id": "1", "email": "e@x.com"}) is False


def test_circuit_breaker_opens() -> None:
    mod = load_module(Path(__file__).resolve().parents[1] / "circuit-breaker" / "example.py")
    cb = mod.CircuitBreaker(threshold=2)

    def boom():
        raise RuntimeError("x")

    for _ in range(2):
        try:
            cb.call(boom)
        except RuntimeError:
            pass

    raised = False
    try:
        cb.call(boom)
    except RuntimeError:
        raised = True
    assert raised
