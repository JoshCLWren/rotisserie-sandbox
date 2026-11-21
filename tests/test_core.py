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


def test_total_by_month_groups_entries_in_month_order() -> None:
    ledger = Ledger()
    ledger.add(Entry(date(2026, 2, 1), Decimal("1.25"), "food"))
    ledger.add(Entry(date(2026, 1, 20), Decimal("4.00"), "travel"))
    ledger.add(Entry(date(2026, 1, 5), Decimal("2.50"), "food"))
    ledger.add(Entry(date(2025, 12, 31), Decimal("0.75"), "food"))

    assert list(ledger.total_by_month().items()) == [
        ("2025-12", Decimal("0.75")),
        ("2026-01", Decimal("6.50")),
        ("2026-02", Decimal("1.25")),
    ]


def test_empty_ledger_has_no_monthly_totals() -> None:
    assert Ledger().total_by_month() == {}
