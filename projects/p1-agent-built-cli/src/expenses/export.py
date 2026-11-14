"""CSV export. Implements SPEC.md, section "CSV export"."""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable

from expenses.store import Expense

COLUMNS = ("date", "category", "amount", "currency", "note")
# Characters that make spreadsheet apps treat a cell as a formula (CSV injection).
FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(value: str) -> str:
    """Neutralize spreadsheet formulas by prefixing a single quote.

    A note like `=HYPERLINK("http://evil.example", "click")` would otherwise run as a formula
    when finance opens the file in Excel. This is a classic thing agents forget.
    """
    return "'" + value if value.startswith(FORMULA_PREFIXES) else value


def to_csv(expenses: Iterable[Expense]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(COLUMNS)
    for e in expenses:
        writer.writerow([e.date, e.category, e.amount, e.currency, safe_cell(e.note)])
    return buffer.getvalue()
