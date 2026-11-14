# AGENTS.md

Instructions for coding agents working in this project. Humans: this is also a good summary of how the project works.

## Commands

- Install: `uv sync`
- Test: `uv run pytest -q` (must pass before you say you're done)
- Lint: `uv run ruff check .` (must pass)
- Try it: `EXPENSES_FILE=/tmp/e.jsonl uv run expenses add 2026-10-03 food 450`

## Layout

- `src/expenses/store.py` data model, validation, JSON Lines storage
- `src/expenses/export.py` CSV export
- `src/expenses/cli.py` argument parsing and output only; no business logic here
- `tests/test_acceptance.py` one test per acceptance criterion in `SPEC.md`
- `tests/test_store.py` unit tests

## Rules

- `SPEC.md` is the source of truth. If a request conflicts with it, stop and ask.
- Write or update a failing test before changing behavior. Never weaken an existing test to make it pass; ask instead.
- Money is `decimal.Decimal` or a string, never `float`.
- No new runtime dependencies. The standard library is enough.
- Don't read or write anything outside the project folder and the temp directory, except the user's data file.
- Show the diff and stop. Don't commit or push.

## Skills

- `.agents/skills/add-command/` how to add a new subcommand the way this project does it.
