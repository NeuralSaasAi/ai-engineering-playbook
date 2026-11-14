"""Command-line interface.

    expenses add 2026-10-03 food 450.50 --note "team lunch"
    expenses list --month 2026-10
    expenses summary --month 2026-10
    expenses export --format csv --month 2026-10 [--out DIR]

Exit codes: 0 success, 1 invalid input, 2 nothing to export.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from expenses.export import to_csv
from expenses.store import CATEGORIES, Store, ValidationError, make_expense

MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
EXIT_INVALID = 1
EXIT_NO_DATA = 2


def month_arg(value: str) -> str:
    if not MONTH.match(value):
        raise argparse.ArgumentTypeError(f"month must be YYYY-MM, got {value!r}")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="expenses", description="Track expenses from the terminal.")
    parser.add_argument("--file", type=Path, help="data file (default: $EXPENSES_FILE or ~/.expenses.jsonl)")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="record an expense")
    add.add_argument("date", help="YYYY-MM-DD")
    add.add_argument("category", help=f"one of: {', '.join(CATEGORIES)}")
    add.add_argument("amount", help="positive number, up to two decimals")
    add.add_argument("--currency", default="INR")
    add.add_argument("--note", default="")

    for name, help_text in (("list", "list a month's expenses"), ("summary", "totals per category")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--month", type=month_arg, required=True)

    export = sub.add_parser("export", help="export a month to a file")
    export.add_argument("--format", choices=["csv"], default="csv")
    export.add_argument("--month", type=month_arg, required=True)
    export.add_argument("--out", type=Path, default=Path("."), help="output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = Store(args.file)

    try:
        if args.command == "add":
            expense = make_expense(args.date, args.category, args.amount, args.currency, args.note)
            store.add(expense)
            print(f"Added {expense.amount} {expense.currency} ({expense.category}) on {expense.date}")
            return 0

        expenses = store.for_month(args.month)

        if args.command == "list":
            for e in expenses:
                print(f"{e.date}  {e.category:<10} {e.amount:>10} {e.currency}  {e.note}")
            return 0

        if args.command == "summary":
            totals: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
            for e in expenses:
                totals[(e.category, e.currency)] += e.amount_decimal
            for (category, currency), total in sorted(totals.items()):
                print(f"{category:<10} {total:>10.2f} {currency}")
            return 0

        if args.command == "export":
            if not expenses:
                print(f"No expenses recorded for {args.month}; nothing exported.", file=sys.stderr)
                return EXIT_NO_DATA
            args.out.mkdir(parents=True, exist_ok=True)
            target = args.out / f"expenses-{args.month}.csv"
            target.write_text(to_csv(expenses), encoding="utf-8")
            print(f"Wrote {len(expenses)} expenses to {target}")
            return 0
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_INVALID

    return EXIT_INVALID  # unreachable: argparse enforces a known command


if __name__ == "__main__":
    sys.exit(main())
