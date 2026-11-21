"""Command line interface."""

from __future__ import annotations

import argparse
import json
import sys
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


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    command = list(argv)
    if "--file" in command:
        index = command.index("--file")
        del command[index : index + 2]
    if command[:1] == ["months"]:
        book = Path("ledger.json")
        if "--file" in argv:
            book = Path(argv[argv.index("--file") + 1])
        for month, total in load(book).total_by_month().items():
            print(f"{month}  {total}")
        return 0
    parser = argparse.ArgumentParser(prog="ledger")
    parser.add_argument("--file", type=Path, default=Path("ledger.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="record an expense")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--note", default="")
    add.add_argument("--day", default=date.today().isoformat())
    sub.add_parser("total", help="print the total of all expenses")
    args = parser.parse_args(argv)

    ledger = load(args.file)
    if args.command == "add":
        ledger.add(
            Entry(date.fromisoformat(args.day), Decimal(args.amount), args.category, args.note)
        )
        save(ledger, args.file)
        return 0
    print(ledger.total())
    return 0
