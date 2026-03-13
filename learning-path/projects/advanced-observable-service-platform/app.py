"""Observable service platform starter."""

import json
from datetime import datetime, timezone


def log(event: str, **context: object) -> None:
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **context,
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    log("boot", service="observable-platform", version="0.1.0")
    print("Expose /health, /metrics, and /api routes in the next step.")
