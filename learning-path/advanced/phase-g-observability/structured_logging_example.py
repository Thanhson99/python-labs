"""Phase G: structured logging example."""

import json
from datetime import datetime, timezone


def log(event: str, **context: object) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **context,
    }
    print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    log("order_created", service="billing", trace_id="abc-123", amount=99.5)
