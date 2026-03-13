"""Circuit breaker simple implementation."""


class CircuitBreaker:
    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.failures = 0

    def call(self, fn):
        if self.failures >= self.threshold:
            raise RuntimeError("circuit open")
        try:
            result = fn()
            self.failures = 0
            return result
        except Exception:  # noqa: BLE001
            self.failures += 1
            raise
