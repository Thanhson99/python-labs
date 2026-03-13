"""Dataclass validation with __post_init__."""

from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    price: float

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("price must be non-negative")


if __name__ == "__main__":
    print(Product("SKU-1", 9.5))
