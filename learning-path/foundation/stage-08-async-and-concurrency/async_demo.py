"""Stage 08: asyncio parallel tasks."""

import asyncio


async def fetch_mock(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done in {delay}s"


async def main() -> None:
    results = await asyncio.gather(
        fetch_mock("job-a", 0.8),
        fetch_mock("job-b", 0.4),
        fetch_mock("job-c", 0.2),
    )
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
