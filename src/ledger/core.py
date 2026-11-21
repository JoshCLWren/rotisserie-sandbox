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

    def total(self, category: str | None = None) -> Decimal:
        entries = self.entries
        if category is not None:
            entries = [entry for entry in entries if entry.category == category]
        return sum((entry.amount for entry in entries), Decimal("0"))
