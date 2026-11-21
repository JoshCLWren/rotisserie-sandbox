from datetime import date
from decimal import Decimal

from ledger import Entry, Ledger


def test_total_sums_every_entry() -> None:
    ledger = Ledger()
    ledger.add(Entry(date(2026, 1, 1), Decimal("2.50"), "food"))
    ledger.add(Entry(date(2026, 1, 2), Decimal("4.00"), "travel"))
    assert ledger.total() == Decimal("6.50")


def test_empty_ledger_totals_zero() -> None:
    assert Ledger().total() == Decimal("0")


def test_total_by_category_sums_per_category() -> None:
    ledger = Ledger()
    ledger.add(Entry(date(2026, 1, 1), Decimal("2.50"), "food"))
    ledger.add(Entry(date(2026, 1, 2), Decimal("4.00"), "travel"))
    ledger.add(Entry(date(2026, 1, 3), Decimal("1.50"), "food"))
    assert ledger.total_by_category() == {"food": Decimal("4.00"), "travel": Decimal("4.00")}


def test_total_by_category_empty_ledger() -> None:
    assert Ledger().total_by_category() == {}
