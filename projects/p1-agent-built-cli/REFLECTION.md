# Reflection: what the agent got wrong

> [!NOTE]
> Keep a log like this for every project you build with an agent. It's the fastest way to learn what to put in `AGENTS.md`, what to check in review, and what to tell an interviewer when they ask how you work with AI.
>
> This is a **worked example**. The mistakes below are ones coding agents commonly make on a task like this, and each one is covered by a test or rule in this project. When you rebuild P1, replace them with what your agent actually did.

## The workflow being reflected on

1. Write [SPEC.md](SPEC.md) by hand.
2. Ask the agent for a plan without code. Correct the plan.
3. Ask the agent to write [tests/test_acceptance.py](tests/test_acceptance.py) from the acceptance criteria. Review every assertion.
4. Ask the agent to implement until the tests pass, then run `ruff` and `pytest` yourself.
5. Review the full diff. If you find a gap, add an acceptance criterion and repeat steps 3 to 5.

## What went wrong, and the fix

| # | What the agent did | Why it matters | What changed |
|---|---|---|---|
| 1 | The first plan stored amounts as `float`. | `0.1 + 0.2 != 0.3` in floating point. Money totals drift. | Plan corrected. Added "Money is Decimal or string, never float" to `AGENTS.md`. |
| 2 | The first plan put the CSV-writing logic inside `cli.py`. | Logic in the CLI layer is hard to test and reuse. | Plan corrected. Layout rules added to `AGENTS.md`. |
| 3 | The first draft of AC4's test only checked that the file contained the word `airport`. | The test would pass even if escaping were broken. A test that can't fail proves nothing. | Rewrote the test to read the file back with `csv.reader` and compare exact values. |
| 4 | The export wrote notes as-is. A note like `=HYPERLINK(...)` becomes a live formula when opened in Excel (**CSV injection**). | Finance opens these files. This is a real attack class ([OWASP](https://owasp.org/www-community/attacks/CSV_Injection)). | Added AC6 to the spec, a failing test, then `safe_cell()`. Added a checklist item to the skill. |
| 5 | `make_expense` accepted `NaN` and `Infinity` as amounts, because `Decimal("NaN")` parses. | Garbage data would break every total. | Added a test case, then an `is_finite()` check. |

## Lessons for next time

- **Review the plan before the code.** Problems 1 and 2 cost a minute each to fix in the plan. In code they would have touched every file.
- **Review the tests as carefully as the code.** Problem 3 would have hidden a real bug.
- **Ask "who opens this output, and with what?"** Problem 4 isn't in any spec unless you think about the consumer. Agents rarely ask.
- **Edge-case inputs are cheap to list.** Ask the agent: "List 10 inputs that could break `make_expense`." It found problem 5 itself when asked directly.
- **Every repeated correction becomes a line in `AGENTS.md` or a skill.**
