"""Stage 05: scheduler demo without external dependencies."""

import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)


def job(counter: int = 1) -> None:
    print(f"tick #{counter}")
    if counter < 5:
        scheduler.enter(1, 1, job, argument=(counter + 1,))


def main() -> None:
    scheduler.enter(0, 1, job)
    scheduler.run()
    print("scheduler completed")


if __name__ == "__main__":
    main()
