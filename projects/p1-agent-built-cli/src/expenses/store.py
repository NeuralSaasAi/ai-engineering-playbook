"""Storage: expenses live in a JSON Lines file, one expense per line.

JSON Lines keeps the format human-readable and append-only, which makes it easy to inspect
what the agent (or you) wrote.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

CATEGORIES = ("food", "travel", "rent", "utilities", "health", "other")
DEFAULT_CURRENCY = "INR"


class ValidationError(ValueError):
    """Raised when user input can't be turned into a valid expense."""


@dataclass(frozen=True)
class Expense:
    date: str  # ISO date, YYYY-MM-DD
    category: str
    amount: str  # stored as a string to keep Decimal precision exact
    currency: str = DEFAULT_CURRENCY
    note: str = ""

    @property
    def amount_decimal(self) -> Decimal:
        return Decimal(self.amount)

    @property
    def month(self) -> str:
        return self.date[:7]


def make_expense(
    when: str, category: str, amount: str, currency: str = DEFAULT_CURRENCY, note: str = ""
) -> Expense:
    """Validate raw strings from the command line and build an Expense."""
    try:
        parsed_date = date.fromisoformat(when)
    except ValueError as exc:
        raise ValidationError(f"date must be YYYY-MM-DD, got {when!r}") from exc

    category = category.strip().lower()
    if category not in CATEGORIES:
        raise ValidationError(f"category must be one of {', '.join(CATEGORIES)}; got {category!r}")

    try:
        value = Decimal(amount)
    except InvalidOperation as exc:
        raise ValidationError(f"amount must be a number, got {amount!r}") from exc
    if not value.is_finite() or value <= 0:
        raise ValidationError("amount must be a positive number")
    if value.as_tuple().exponent < -2:  # type: ignore[operator]
        raise ValidationError("amount can have at most two decimal places")

    currency = currency.strip().upper()
    if len(currency) != 3 or not currency.isalpha():
        raise ValidationError(f"currency must be a 3-letter code like INR or USD, got {currency!r}")

    return Expense(
        date=parsed_date.isoformat(),
        category=category,
        amount=f"{value:.2f}",
        currency=currency,
        note=note.strip(),
    )


def default_path() -> Path:
    return Path(os.environ.get("EXPENSES_FILE", Path.home() / ".expenses.jsonl"))


class Store:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_path()

    def add(self, expense: Expense) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(expense), ensure_ascii=False) + "\n")

    def all(self) -> list[Expense]:
        if not self.path.exists():
            return []
        expenses = []
        with self.path.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    expenses.append(Expense(**json.loads(line)))
                except (json.JSONDecodeError, TypeError) as exc:
                    raise ValidationError(f"{self.path}:{line_no} is not a valid expense record") from exc
        return expenses

    def for_month(self, month: str) -> list[Expense]:
        return sorted((e for e in self.all() if e.month == month), key=lambda e: e.date)
