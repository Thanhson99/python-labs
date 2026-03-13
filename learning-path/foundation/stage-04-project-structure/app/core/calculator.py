"""Core business logic."""


def convert_price(amount: float, exchange_rate: float) -> float:
    return round(amount * exchange_rate, 2)
