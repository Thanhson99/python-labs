"""Entrypoint composition example."""

from config import load_config
from core.calculator import convert_price


def main() -> None:
    config = load_config()
    converted = convert_price(19.99, 1.08)
    print({"app": config.app_name, "currency": config.default_currency, "value": converted})


if __name__ == "__main__":
    main()
