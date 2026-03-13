"""Phase D: repository interface and in-memory implementation."""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Invoice:
    id: str
    amount: float


class InvoiceRepository(Protocol):
    def save(self, invoice: Invoice) -> None: ...
    def get(self, invoice_id: str) -> Invoice | None: ...


class InMemoryInvoiceRepository:
    def __init__(self) -> None:
        self._store: dict[str, Invoice] = {}

    def save(self, invoice: Invoice) -> None:
        self._store[invoice.id] = invoice

    def get(self, invoice_id: str) -> Invoice | None:
        return self._store.get(invoice_id)


if __name__ == "__main__":
    repo = InMemoryInvoiceRepository()
    repo.save(Invoice(id="inv-1", amount=149.99))
    print(repo.get("inv-1"))
