import csv
from pathlib import Path

from ledger.cli import main


def test_export_csv_round_trip(tmp_path: Path) -> None:
    book = tmp_path / "ledger.json"
    out = tmp_path / "ledger.csv"
    assert (
        main(
            [
                "--file",
                str(book),
                "add",
                "3.25",
                "food",
                "--day",
                "2026-01-01",
                "--note",
                "lunch, with tea",
            ]
        )
        == 0
    )
    assert main(["--file", str(book), "add", "1.75", "travel", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "export", "--csv", str(out)]) == 0

    text = out.read_text()
    assert text.splitlines()[0] == "day,amount,category,note"
    assert '"lunch, with tea"' in text

    with out.open(newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == ["day", "amount", "category", "note"]
        rows = list(reader)

    assert rows == [
        {
            "day": "2026-01-01",
            "amount": "3.25",
            "category": "food",
            "note": "lunch, with tea",
        },
        {"day": "2026-01-02", "amount": "1.75", "category": "travel", "note": ""},
    ]
