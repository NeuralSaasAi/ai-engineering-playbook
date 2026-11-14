"""Acceptance tests: one test per acceptance criterion in SPEC.md.

These were written BEFORE the implementation, so the agent had a fixed target.
If you change behavior, change SPEC.md first, then these tests, then the code.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from expenses.cli import main


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    return tmp_path / "expenses.jsonl"


def run(data_file: Path, *args: str) -> int:
    return main(["--file", str(data_file), *args])


def seed(data_file: Path) -> None:
    run(data_file, "add", "2026-10-03", "food", "450.5", "--note", "team lunch")
    run(data_file, "add", "2026-10-01", "travel", "1200", "--note", 'cab, airport "early"')
    run(data_file, "add", "2026-09-30", "rent", "25000")  # different month, must be excluded


def read_csv(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


# AC1: `expenses export --format csv --month 2026-10` writes `expenses-2026-10.csv`
def test_ac1_export_writes_named_file(data_file, tmp_path):
    seed(data_file)
    assert run(data_file, "export", "--format", "csv", "--month", "2026-10", "--out", str(tmp_path)) == 0
    assert (tmp_path / "expenses-2026-10.csv").exists()


# AC2: columns are date, category, amount, currency, note, with a header row; only that month, sorted by date
def test_ac2_columns_header_and_month_filter(data_file, tmp_path):
    seed(data_file)
    run(data_file, "export", "--month", "2026-10", "--out", str(tmp_path))
    rows = read_csv(tmp_path / "expenses-2026-10.csv")
    assert rows[0] == ["date", "category", "amount", "currency", "note"]
    assert [r[0] for r in rows[1:]] == ["2026-10-01", "2026-10-03"]


# AC3: amounts use a dot decimal separator and two decimal places
def test_ac3_amount_format(data_file, tmp_path):
    seed(data_file)
    run(data_file, "export", "--month", "2026-10", "--out", str(tmp_path))
    amounts = [r[2] for r in read_csv(tmp_path / "expenses-2026-10.csv")[1:]]
    assert amounts == ["1200.00", "450.50"]


# AC4: notes containing commas or quotes are escaped correctly (they round-trip through a CSV reader)
def test_ac4_notes_with_commas_and_quotes_round_trip(data_file, tmp_path):
    seed(data_file)
    run(data_file, "export", "--month", "2026-10", "--out", str(tmp_path))
    notes = [r[4] for r in read_csv(tmp_path / "expenses-2026-10.csv")[1:]]
    assert notes == ['cab, airport "early"', "team lunch"]


# AC5: exits with code 2 and a clear message if the month has no data
def test_ac5_no_data_exit_code(data_file, tmp_path, capsys):
    seed(data_file)
    assert run(data_file, "export", "--month", "2026-11", "--out", str(tmp_path)) == 2
    assert "No expenses recorded for 2026-11" in capsys.readouterr().err
    assert not (tmp_path / "expenses-2026-11.csv").exists()


# AC6 (added after review, see REFLECTION.md): notes that look like spreadsheet formulas are neutralized
def test_ac6_csv_formula_injection_is_neutralized(data_file, tmp_path):
    run(data_file, "add", "2026-10-05", "other", "10", "--note", '=HYPERLINK("http://evil.example","x")')
    run(data_file, "export", "--month", "2026-10", "--out", str(tmp_path))
    note = read_csv(tmp_path / "expenses-2026-10.csv")[1][4]
    assert note.startswith("'=")
