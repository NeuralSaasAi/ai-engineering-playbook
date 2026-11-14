"""Unit tests for input validation and storage."""

from __future__ import annotations

import pytest

from expenses.cli import main
from expenses.store import Store, ValidationError, make_expense


def test_valid_expense_is_normalized():
    e = make_expense("2026-10-03", " Food ", "450.5", "inr", "  lunch ")
    got = (e.date, e.category, e.amount, e.currency, e.note)
    assert got == ("2026-10-03", "food", "450.50", "INR", "lunch")


@pytest.mark.parametrize(
    ("when", "category", "amount", "currency", "message"),
    [
        ("03-10-2026", "food", "10", "INR", "YYYY-MM-DD"),
        ("2026-10-03", "snacks", "10", "INR", "category"),
        ("2026-10-03", "food", "ten", "INR", "number"),
        ("2026-10-03", "food", "-5", "INR", "positive"),
        ("2026-10-03", "food", "0", "INR", "positive"),
        ("2026-10-03", "food", "NaN", "INR", "positive"),
        ("2026-10-03", "food", "1.234", "INR", "two decimal"),
        ("2026-10-03", "food", "10", "RUPEES", "3-letter"),
    ],
)
def test_invalid_input_is_rejected(when, category, amount, currency, message):
    with pytest.raises(ValidationError, match=message):
        make_expense(when, category, amount, currency)


def test_store_round_trip_preserves_unicode(tmp_path):
    store = Store(tmp_path / "e.jsonl")
    store.add(make_expense("2026-10-03", "food", "120", note="चाय और समोसा"))
    assert store.all()[0].note == "चाय और समोसा"


def test_corrupt_line_gives_clear_error(tmp_path):
    path = tmp_path / "e.jsonl"
    path.write_text("not json\n", encoding="utf-8")
    with pytest.raises(ValidationError, match=":1 is not a valid expense"):
        Store(path).all()


def test_cli_rejects_bad_input_with_exit_code_1(tmp_path, capsys):
    assert main(["--file", str(tmp_path / "e.jsonl"), "add", "2026-10-03", "food", "-1"]) == 1
    assert "Error: amount must be a positive number" in capsys.readouterr().err


def test_summary_totals_per_category(tmp_path, capsys):
    f = str(tmp_path / "e.jsonl")
    main(["--file", f, "add", "2026-10-01", "food", "100.10"])
    main(["--file", f, "add", "2026-10-02", "food", "0.20"])
    main(["--file", f, "add", "2026-10-02", "travel", "50"])
    capsys.readouterr()
    assert main(["--file", f, "summary", "--month", "2026-10"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out == ["food           100.30 INR", "travel          50.00 INR"]


def test_month_argument_is_validated(tmp_path):
    with pytest.raises(SystemExit):
        main(["--file", str(tmp_path / "e.jsonl"), "list", "--month", "2026-13"])
