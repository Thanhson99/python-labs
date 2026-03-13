"""Stage 08: thread pool for blocking tasks."""

from concurrent.futures import ThreadPoolExecutor
import time


def blocking_task(value: int) -> int:
    time.sleep(0.4)
    return value * value


def main() -> None:
    with ThreadPoolExecutor(max_workers=4) as pool:
        result = list(pool.map(blocking_task, [2, 3, 4, 5]))
    print(result)


if __name__ == "__main__":
    main()
