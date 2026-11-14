# Spec: expenses CLI

> [!NOTE]
> This is the spec the coding agent was given. Write yours like this: problem, users, acceptance criteria you can test, and what's out of scope. Each acceptance criterion maps to one test in [tests/test_acceptance.py](tests/test_acceptance.py).

## Problem

A small team tracks shared expenses in a chat thread. At month end, someone copies everything into a spreadsheet by hand for finance. It takes an hour and has errors.

## Users

Team members who are comfortable in a terminal. Finance, who only sees the exported file.

## Commands

| Command | Does |
|---|---|
| `expenses add DATE CATEGORY AMOUNT [--currency INR] [--note TEXT]` | Records one expense |
| `expenses list --month YYYY-MM` | Lists that month's expenses, oldest first |
| `expenses summary --month YYYY-MM` | Totals per category and currency |
| `expenses export --format csv --month YYYY-MM [--out DIR]` | Writes the month to a CSV file |

Data is stored as JSON Lines in `$EXPENSES_FILE`, defaulting to `~/.expenses.jsonl`.

## Validation

- Date is `YYYY-MM-DD`. Category is one of: food, travel, rent, utilities, health, other.
- Amount is a positive number with at most two decimals. Use exact decimal arithmetic, never floats, for money.
- Currency is a 3-letter code. Default INR.
- Invalid input prints `Error: <reason>` to stderr and exits with code 1.

## CSV export: acceptance criteria

- [x] **AC1** `expenses export --format csv --month 2026-10` writes `expenses-2026-10.csv`
- [x] **AC2** Columns: date, category, amount, currency, note (in that order, with a header row). Only the requested month, sorted by date
- [x] **AC3** Amounts use a dot decimal separator and two decimal places
- [x] **AC4** Notes containing commas or quotes are escaped correctly
- [x] **AC5** Exits with code 2 and a clear message if the month has no data
- [x] **AC6** Notes that start with `=`, `+`, `-` or `@` are neutralized so spreadsheets don't run them as formulas *(added during review, see [REFLECTION.md](REFLECTION.md))*

## Out of scope

Excel (.xlsx) output, multiple users, editing or deleting entries, currency conversion.
