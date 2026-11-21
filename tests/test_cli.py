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


def test_add_rejects_zero_amount(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "0", "food"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "amount must be positive" in captured.err
    assert not book.exists()


def test_add_rejects_negative_amount_and_leaves_file_unchanged(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    before = book.read_text()
    capsys.readouterr()
    assert main(["--file", str(book), "add", "-2", "food"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "amount must be positive" in captured.err
    assert book.read_text() == before
