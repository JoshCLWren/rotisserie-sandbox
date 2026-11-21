from datetime import date
from decimal import Decimal

import pytest

from ledger import Entry, Ledger


def test_total_sums_every_entry() -> None:
    ledger = Ledger()
    ledger.add(Entry(date(2026, 1, 1), Decimal("2.50"), "food"))
    ledger.add(Entry(date(2026, 1, 2), Decimal("4.00"), "travel"))
    assert ledger.total() == Decimal("6.50")


def test_empty_ledger_totals_zero() -> None:
    assert Ledger().total() == Decimal("0")


def test_entry_rejects_zero_amount() -> None:
    with pytest.raises(ValueError):
        Entry(date(2026, 1, 1), Decimal("0"), "food")


def test_entry_rejects_negative_amount() -> None:
    with pytest.raises(ValueError):
        Entry(date(2026, 1, 1), Decimal("-2"), "food")
