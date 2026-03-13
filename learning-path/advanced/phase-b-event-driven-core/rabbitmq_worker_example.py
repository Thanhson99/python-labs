"""Phase B: RabbitMQ worker structure example."""

# Example only. Requires pika + running RabbitMQ to execute for real.


def publish_order_created(order_id: str) -> dict:
    message = {"event": "order_created", "order_id": order_id}
    return message


def consume_order_created(message: dict) -> str:
    return f"consume event={message['event']} order_id={message['order_id']}"


if __name__ == "__main__":
    payload = publish_order_created("order-1001")
    print(consume_order_created(payload))
