from datetime import date
from decimal import Decimal

import pytest

from ledger import Entry, Ledger


def test_package_version() -> None:
    import ledger

    assert ledger.__version__ == "0.1.0"


def test_total_sums_every_entry() -> None:
    ledger = Ledger()
    ledger.add(Entry(date(2026, 1, 1), Decimal("2.50"), "food"))
    ledger.add(Entry(date(2026, 1, 2), Decimal("4.00"), "travel"))
    assert ledger.total() == Decimal("6.50")


def test_count_returns_number_of_entries() -> None:
    ledger = Ledger()
    assert ledger.count() == 0
    ledger.add(Entry(date(2026, 1, 1), Decimal("2.50"), "food"))
    ledger.add(Entry(date(2026, 1, 2), Decimal("4.00"), "travel"))
    assert ledger.count() == 2
    assert isinstance(ledger.count(), int)


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


def test_category_is_lowercased() -> None:
    entry = Entry(date(2026, 1, 1), Decimal("2.50"), "Food")
    assert entry.category == "food"


def test_category_is_stripped_of_surrounding_spaces() -> None:
    entry = Entry(date(2026, 1, 1), Decimal("2.50"), "  food  ")
    assert entry.category == "food"


def test_mixed_case_with_surrounding_spaces_is_normalized() -> None:
    entry = Entry(date(2026, 1, 1), Decimal("2.50"), "  TrAvEl ")
    assert entry.category == "travel"


def test_empty_category_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Entry(date(2026, 1, 1), Decimal("2.50"), "")


def test_blank_category_after_stripping_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Entry(date(2026, 1, 1), Decimal("2.50"), "   ")


def test_is_empty_returns_true_when_no_entries() -> None:
    assert Ledger().is_empty() is True


def test_is_empty_returns_false_after_adding_entry() -> None:
    ledger = Ledger()
    ledger.add(Entry(date(2026, 1, 1), Decimal("2.50"), "food"))
    assert ledger.is_empty() is False
