from datetime import date
from decimal import Decimal

from ledger import Entry, Ledger


def test_package_version() -> None:
    import ledger

    assert ledger.__version__ == "0.1.0"


def test_total_sums_every_entry() -> None:
    ledger = Ledger()
    ledger.add(Entry(date(2026, 1, 1), Decimal("2.50"), "food"))
    ledger.add(Entry(date(2026, 1, 2), Decimal("4.00"), "travel"))
    assert ledger.total() == Decimal("6.50")


def test_empty_ledger_totals_zero() -> None:
    assert Ledger().total() == Decimal("0")
