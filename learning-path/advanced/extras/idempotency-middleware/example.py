"""Idempotency key handler sample."""


class IdempotencyStore:
    def __init__(self):
        self._store = {}

    def handle(self, key: str, fn):
        if key in self._store:
            return self._store[key]
        result = fn()
        self._store[key] = result
        return result


if __name__ == "__main__":
    store = IdempotencyStore()
    n = {"count": 0}

    def op():
        n["count"] += 1
        return {"ok": True, "count": n["count"]}

    print(store.handle("k1", op))
    print(store.handle("k1", op))
