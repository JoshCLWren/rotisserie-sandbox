"""Command line interface."""

from __future__ import annotations

import argparse
import json
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from ledger.core import Entry, Ledger


def _positive_amount(raw: str) -> Decimal:
    try:
        amount = Decimal(raw)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError(f"invalid amount: {raw}") from exc
    if amount <= Decimal("0"):
        raise argparse.ArgumentTypeError("amount must be positive")
    return amount


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
    parser = argparse.ArgumentParser(prog="ledger")
    parser.add_argument("--file", type=Path, default=Path("ledger.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="record an expense")
    add.add_argument("amount", type=_positive_amount)
    add.add_argument("category")
    add.add_argument("--note", default="")
    add.add_argument("--day", default=date.today().isoformat())
    sub.add_parser("total", help="print the total of all expenses")
    sub.add_parser("list", help="list every expense, oldest day first")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return code if isinstance(code, int) else 1

    ledger = load(args.file)
    if args.command == "add":
        ledger.add(Entry(date.fromisoformat(args.day), args.amount, args.category, args.note))
        save(ledger, args.file)
        return 0
    if args.command == "list":
        entries = sorted(ledger.entries, key=lambda entry: entry.day)
        if not entries:
            print("No expenses recorded.")
        else:
            for entry in entries:
                print(f"{entry.day.isoformat()}  {entry.amount}  {entry.category}  {entry.note}")
        return 0
    print(ledger.total())
    return 0
