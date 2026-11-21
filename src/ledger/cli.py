"""Command line interface."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from ledger.core import Entry, Ledger

REQUIRED_FIELDS = ("day", "amount", "category")


class LedgerReadError(Exception):
    """Raised when a ledger file cannot be read or decoded."""


def _read_entry(row: object, number: int) -> Entry:
    if not isinstance(row, dict):
        raise LedgerReadError(f"row {number} is not an object")
    for name in REQUIRED_FIELDS:
        if name not in row:
            raise LedgerReadError(f"row {number} is missing field {name!r}")
    try:
        day = date.fromisoformat(row["day"])
    except (TypeError, ValueError) as exc:
        raise LedgerReadError(f"row {number} has an invalid day: {row['day']!r}") from exc
    try:
        amount = Decimal(str(row["amount"]))
    except (InvalidOperation, TypeError) as exc:
        raise LedgerReadError(f"row {number} has an invalid amount: {row['amount']!r}") from exc
    category = row["category"]
    note = row.get("note", "")
    if not isinstance(category, str) or not isinstance(note, str):
        raise LedgerReadError(f"row {number} has an invalid category or note")
    return Entry(day, amount, category, note)


def load(path: Path) -> Ledger:
    if not path.exists():
        return Ledger()
    try:
        rows = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise LedgerReadError(f"invalid JSON: {exc}") from exc
    except (OSError, UnicodeError) as exc:
        raise LedgerReadError(str(exc)) from exc
    if not isinstance(rows, list):
        raise LedgerReadError("expected a JSON array of entries")
    return Ledger([_read_entry(row, number) for number, row in enumerate(rows, start=1)])


def save(ledger: Ledger, path: Path) -> None:
    rows = [
        {"day": e.day.isoformat(), "amount": str(e.amount), "category": e.category, "note": e.note}
        for e in ledger.entries
    ]
    path.write_text(json.dumps(rows, indent=2) + "\n")


def export_csv(ledger: Ledger, path: Path) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["day", "amount", "category", "note"])
        for entry in ledger.entries:
            writer.writerow([entry.day.isoformat(), str(entry.amount), entry.category, entry.note])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ledger")
    parser.add_argument("--file", type=Path, default=Path("ledger.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="record an expense")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--note", default="")
    add.add_argument("--day", default=date.today().isoformat())
<<<<<<< HEAD
    sub.add_parser("total", help="print the total of all expenses")
    export = sub.add_parser("export", help="write the ledger to CSV")
    export.add_argument("--csv", type=Path, required=True, help="destination CSV path")
=======
    total_parser = sub.add_parser("total", help="print the total of all expenses")
    total_parser.add_argument(
        "--category",
        default=None,
        help="total only entries in this category",
    )
    sub.add_parser("list", help="list every expense, oldest day first")
>>>>>>> origin/main
    args = parser.parse_args(argv)

    try:
        ledger = load(args.file)
    except LedgerReadError as exc:
        print(f"ledger: cannot read {args.file}: {exc}", file=sys.stderr)
        return 1
    if args.command == "add":
        ledger.add(
            Entry(date.fromisoformat(args.day), Decimal(args.amount), args.category, args.note)
        )
        save(ledger, args.file)
        return 0
<<<<<<< HEAD
    if args.command == "export":
        export_csv(ledger, args.csv)
        return 0
    print(ledger.total())
=======
    if args.command == "list":
        entries = sorted(ledger.entries, key=lambda entry: entry.day)
        if not entries:
            print("No expenses recorded.")
        else:
            for entry in entries:
                print(f"{entry.day.isoformat()}  {entry.amount}  {entry.category}  {entry.note}")
        return 0
    entries = ledger.entries
    if args.category is not None:
        category = args.category.strip().lower()
        entries = [entry for entry in entries if entry.category == category]
    print(sum((entry.amount for entry in entries), Decimal("0")))
>>>>>>> origin/main
    return 0
