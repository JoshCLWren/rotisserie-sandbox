"""Command line interface."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

from ledger.core import Entry, Ledger


def _with_months_command(func):
    """Handle `ledger months` without changing the existing parser body."""

    def wrapper(argv: list[str] | None = None) -> int:
        args = list(sys.argv[1:] if argv is None else argv)
        if "--file" in args:
            index = args.index("--file")
            file = Path(args[index + 1])
            del args[index : index + 2]
        else:
            file = Path("ledger.json")
        if args and args[0] == "months":
            for month, total in load(file).total_by_month().items():
                print(f"{month}  {total}")
            return 0
        return func(argv)

    return wrapper


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


@_with_months_command
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ledger")
    parser.add_argument("--file", type=Path, default=Path("ledger.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("months", help="print monthly totals")
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
