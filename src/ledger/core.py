"""Ledger entries and totals."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Entry:
    day: date
    amount: Decimal
    category: str
    note: str = ""

    def __post_init__(self) -> None:
        normalized = self.category.strip().lower()
        if not normalized:
            raise ValueError("category must not be empty")
        object.__setattr__(self, "category", normalized)


@dataclass
class Ledger:
    entries: list[Entry] = field(default_factory=list)

    def add(self, entry: Entry) -> None:
        self.entries.append(entry)

    def total(self) -> Decimal:
        return sum((entry.amount for entry in self.entries), Decimal("0"))

    def total_by_category(self) -> dict[str, Decimal]:
        totals: dict[str, Decimal] = {}
        for entry in self.entries:
            totals[entry.category] = totals.get(entry.category, Decimal("0")) + entry.amount
        return totals