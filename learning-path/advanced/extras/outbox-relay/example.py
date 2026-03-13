"""Outbox relay skeleton."""


def fetch_pending_outbox() -> list[dict]:
    return [{"id": 1, "event": "user_registered"}]


def publish(event: dict) -> None:
    print(f"publish {event}")


def mark_sent(item_id: int) -> None:
    print(f"mark sent {item_id}")


if __name__ == "__main__":
    for item in fetch_pending_outbox():
        publish(item)
        mark_sent(item["id"])
