---
name: add-command
description: Add a new subcommand to the expenses CLI, spec-first and test-first. Use when asked to add a command, flag, report, or export format to the expenses tool.
---

# Add a subcommand to the expenses CLI

Follow these steps in order. Stop after step 2 and show the user the plan before writing code.

1. **Update the spec.** Add the command to the Commands table in `SPEC.md` and write numbered acceptance criteria (`AC7`, `AC8`, ...) that a test can check. Include the exit code for each failure case.
2. **Plan.** List the files you will change and why. Business logic goes in `store.py` or a new module, never in `cli.py`.
3. **Tests first.** Add one test per new acceptance criterion to `tests/test_acceptance.py`, named `test_acN_...`. Run `uv run pytest -q` and confirm the new tests fail for the right reason.
4. **Implement.** Add the subparser in `build_parser()` and a branch in `main()`. Validate input and raise `ValidationError` for bad values so the CLI prints `Error: ...` and exits 1.
5. **Verify.** Run `uv run pytest -q` and `uv run ruff check .`. Both must pass.
6. **Report.** Show the diff, list which acceptance criteria are covered by which tests, and stop. Don't commit.

## Checklist before you finish

- [ ] No floats used for money
- [ ] Any user text written to a file that a spreadsheet may open goes through `safe_cell()`
- [ ] Errors go to stderr; normal output to stdout
- [ ] `README.md` usage section updated if the command is user-facing
