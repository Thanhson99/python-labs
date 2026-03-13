"""Phase B: Kafka producer payload example."""

import json
from datetime import datetime, timezone


def build_event(topic: str, key: str, value: dict) -> bytes:
    payload = {
        "topic": topic,
        "key": key,
        "value": value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload).encode("utf-8")


if __name__ == "__main__":
    event = build_event("orders", "order-1001", {"status": "created"})
    print(event.decode("utf-8"))
