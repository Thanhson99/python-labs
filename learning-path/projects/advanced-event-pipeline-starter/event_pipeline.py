"""Event pipeline milestone starter."""


def producer(order_id: str) -> dict:
    return {"event": "order_created", "order_id": order_id}


def outbox_relay(event: dict) -> dict:
    return {"topic": "orders", "payload": event}


def consumer(record: dict) -> str:
    payload = record["payload"]
    return f"processed event={payload['event']} order_id={payload['order_id']}"


if __name__ == "__main__":
    event = producer("order-5001")
    record = outbox_relay(event)
    print(consumer(record))
