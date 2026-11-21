from pathlib import Path

from ledger.cli import main


def test_add_then_total(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "add", "1.75", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "total"]) == 0
    assert capsys.readouterr().out.strip() == "5.00"


def test_import_csv(tmp_path: Path, capsys) -> None:
    # Create a CSV file with entries
    csv_file = tmp_path / "import.csv"
    csv_file.write_text(
        "day,amount,category,note\n2026-01-01,3.25,food,lunch\n2026-01-02,1.75,coffee,breakfast\n"
    )
    assert main(["--file", str(tmp_path / "ledger.json"), "import", "--csv", str(csv_file)]) == 0
    assert main(["--file", str(tmp_path / "ledger.json"), "total"]) == 0
    out = capsys.readouterr().out.strip()
    assert out == "5.00"


def test_import_csv_then_total_with_existing(tmp_path: Path, capsys) -> None:
    # First add an entry via CLI
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "2.50", "travel", "--day", "2026-01-01"]) == 0
    # Then import more entries from CSV
    csv_file = tmp_path / "import.csv"
    csv_file.write_text("day,amount,category,note\n2026-01-02,3.25,food,lunch\n")
    assert main(["--file", str(book), "import", "--csv", str(csv_file)]) == 0
    assert main(["--file", str(book), "total"]) == 0
    out = capsys.readouterr().out.strip()
    assert out == "5.75"
