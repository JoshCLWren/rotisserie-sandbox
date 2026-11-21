from pathlib import Path

from ledger.cli import main


def test_add_then_total(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "add", "1.75", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "total"]) == 0
    assert capsys.readouterr().out.strip() == "5.00"


def test_list_prints_entries_oldest_day_first(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert (
        main(
            [
                "--file",
                str(book),
                "add",
                "3.25",
                "food",
                "--day",
                "2026-01-02",
                "--note",
                "lunch",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "--file",
                str(book),
                "add",
                "1.75",
                "food",
                "--day",
                "2026-01-01",
                "--note",
                "coffee",
            ]
        )
        == 0
    )
    assert main(["--file", str(book), "list"]) == 0
    assert (
        capsys.readouterr().out == "2026-01-01  1.75  food  coffee\n2026-01-02  3.25  food  lunch\n"
    )


def test_list_with_no_entries(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "list"]) == 0
    assert capsys.readouterr().out == "No expenses recorded.\n"


def test_total_with_category_sums_only_that_category(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "add", "1.75", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "add", "2.50", "travel", "--day", "2026-01-03"]) == 0
    assert main(["--file", str(book), "total", "--category", "food"]) == 0
    assert capsys.readouterr().out.strip() == "5.00"


def test_total_with_unknown_category_prints_zero(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "total", "--category", "car"]) == 0
    assert capsys.readouterr().out.strip() == "0"


def test_total_without_category_still_sums_everything(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "add", "2.50", "travel", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "total"]) == 0
    assert capsys.readouterr().out.strip() == "5.75"


def test_months_prints_one_line_per_month(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "2.50", "food", "--day", "2026-02-03"]) == 0
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "add", "1.75", "travel", "--day", "2026-01-15"]) == 0
    capsys.readouterr()

    assert main(["--file", str(book), "months"]) == 0
    assert capsys.readouterr().out == "2026-01  5.00\n2026-02  2.50\n"
