"""Phase E: retry + lightweight circuit breaker sample."""

import random
import time


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3) -> None:
        self.failure_threshold = failure_threshold
        self.failures = 0

    def allow(self) -> bool:
        return self.failures < self.failure_threshold

    def record_success(self) -> None:
        self.failures = 0

    def record_failure(self) -> None:
        self.failures += 1


def unreliable_call() -> str:
    if random.random() < 0.6:
        raise TimeoutError("upstream timeout")
    return "ok"


def main() -> None:
    breaker = CircuitBreaker()

    for attempt in range(1, 8):
        if not breaker.allow():
            print("circuit open: skip call")
            break

        try:
            result = unreliable_call()
            breaker.record_success()
            print(f"attempt={attempt} result={result}")
            break
        except TimeoutError as exc:
            breaker.record_failure()
            print(f"attempt={attempt} error={exc} failures={breaker.failures}")
            time.sleep(0.3)


if __name__ == "__main__":
    main()
