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


@dataclass
class Ledger:
    entries: list[Entry] = field(default_factory=list)

    def add(self, entry: Entry) -> None:
        self.entries.append(entry)

    def total(self) -> Decimal:
        return sum((entry.amount for entry in self.entries), Decimal("0"))

    def total_by_month(self) -> dict[str, Decimal]:
        monthly: dict[str, Decimal] = {}
        for entry in self.entries:
            month = f"{entry.day.year:04d}-{entry.day.month:02d}"
            monthly[month] = monthly.get(month, Decimal("0")) + entry.amount
        return dict(sorted(monthly.items()))
