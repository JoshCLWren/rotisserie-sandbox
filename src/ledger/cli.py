"""Command line interface."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from ledger.core import Entry, Ledger


def load(path: Path) -> Ledger:
    if not path.exists():
        return Ledger()
    rows = json.loads(path.read_text())
    return Ledger(
        [
            Entry(
                date.fromisoformat(r["day"]), Decimal(r["amount"]), r["category"], r.get("note", "")
            )
            for r in rows
        ]
    )


def save(ledger: Ledger, path: Path) -> None:
    rows = [
        {"day": e.day.isoformat(), "amount": str(e.amount), "category": e.category, "note": e.note}
        for e in ledger.entries
    ]
    path.write_text(json.dumps(rows, indent=2) + "\n")


def export_csv(ledger: Ledger, path: Path) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
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
    sub.add_parser("total", help="print the total of all expenses")
    export = sub.add_parser("export", help="export the ledger as CSV")
    export.add_argument("--csv", type=Path, required=True, help="path of the CSV file to write")
    args = parser.parse_args(argv)

    ledger = load(args.file)
    if args.command == "add":
        ledger.add(
            Entry(date.fromisoformat(args.day), Decimal(args.amount), args.category, args.note)
        )
        save(ledger, args.file)
        return 0
    if args.command == "export":
        export_csv(ledger, args.csv)
        return 0
    print(ledger.total())
    return 0
