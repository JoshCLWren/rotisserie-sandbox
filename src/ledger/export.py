"""CSV export for the ledger."""

from __future__ import annotations

import csv
from pathlib import Path

from ledger.core import Ledger


def export_csv(ledger: Ledger, path: Path) -> None:
    """Write every entry to ``path`` as CSV with a header row."""
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["day", "amount", "category", "note"])
        for entry in ledger.entries:
            writer.writerow([entry.day.isoformat(), str(entry.amount), entry.category, entry.note])
