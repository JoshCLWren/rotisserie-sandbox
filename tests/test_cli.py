from pathlib import Path

from ledger.cli import main


def test_add_then_total(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "add", "1.75", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "total"]) == 0
    assert capsys.readouterr().out.strip() == "5.00"


def test_add_then_total_by_category(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "add", "1.75", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "add", "2.50", "travel", "--day", "2026-01-03"]) == 0
    assert main(["--file", str(book), "total", "--category", "food"]) == 0
    assert capsys.readouterr().out.strip() == "5.00"
    assert main(["--file", str(book), "total", "--category", "travel"]) == 0
    assert capsys.readouterr().out.strip() == "2.50"
