from pathlib import Path

import pytest

from ledger.cli import main


def test_add_then_total(tmp_path: Path, capsys) -> None:
    book = tmp_path / "ledger.json"
    assert main(["--file", str(book), "add", "3.25", "food", "--day", "2026-01-01"]) == 0
    assert main(["--file", str(book), "add", "1.75", "food", "--day", "2026-01-02"]) == 0
    assert main(["--file", str(book), "total"]) == 0
    assert capsys.readouterr().out.strip() == "5.00"


COMMANDS = [
    ["total"],
    ["add", "1.00", "food", "--day", "2026-01-01"],
]


@pytest.mark.parametrize("command", COMMANDS)
def test_invalid_json_reports_clean_error(tmp_path: Path, capsys, command: list[str]) -> None:
    book = tmp_path / "ledger.json"
    book.write_text("{not valid json")

    assert main(["--file", str(book), *command]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith(f"ledger: cannot read {book}: ")
    assert "Traceback" not in captured.err
    assert book.read_text() == "{not valid json"


@pytest.mark.parametrize("command", COMMANDS)
def test_missing_field_reports_clean_error(tmp_path: Path, capsys, command: list[str]) -> None:
    book = tmp_path / "ledger.json"
    book.write_text('[{"day": "2026-01-01", "amount": "1.00"}]')

    assert main(["--file", str(book), *command]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith(f"ledger: cannot read {book}: ")
    assert "missing field 'category'" in captured.err
    assert "Traceback" not in captured.err
