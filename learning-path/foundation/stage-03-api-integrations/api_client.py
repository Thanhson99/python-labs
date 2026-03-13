"""Stage 03: simple API client with retry and timeout."""

from __future__ import annotations

import json
import time
from urllib.error import URLError
from urllib.request import urlopen


def fetch_json(url: str, timeout: int = 10, retries: int = 3) -> dict:
    """Fetch JSON from URL with lightweight retry logic."""
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            with urlopen(url, timeout=timeout) as response:  # nosec B310 - lab sample
                body = response.read().decode("utf-8")
                return json.loads(body)
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            print(f"attempt={attempt} failed: {exc}")
            time.sleep(0.4)

    raise RuntimeError(f"Failed after {retries} retries: {last_error}")


if __name__ == "__main__":
    result = fetch_json("https://api.github.com/repos/python/cpython")
    print({"name": result.get("name"), "stars": result.get("stargazers_count")})
