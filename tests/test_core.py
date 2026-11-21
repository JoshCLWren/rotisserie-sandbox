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


def test_entry_rejects_zero_amount() -> None:
    with pytest.raises(ValueError):
        Entry(date(2026, 1, 1), Decimal("0"), "food")


def test_entry_rejects_negative_amount() -> None:
    with pytest.raises(ValueError):
        Entry(date(2026, 1, 1), Decimal("-2"), "food")
