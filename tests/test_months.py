from datetime import date
from decimal import Decimal
from pathlib import Path

from ledger import Entry, Ledger
from ledger.cli import main


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


def test_months_prints_one_line_per_month(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "2.50", "food", "--day", "2026-02-03"]) == 0
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "add", "1.75", "travel", "--day", "2026-01-15"]) == 0
    capsys.readouterr()

    assert main(["--file", str(book), "months"]) == 0
    assert capsys.readouterr().out == "2026-01  5.00\n2026-02  2.50\n"
