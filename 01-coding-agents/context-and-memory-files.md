---
title: Context, memory files and AGENTS.md
level: beginner
last_reviewed: 2026-11-14
---

# Context, memory files and AGENTS.md

## In one sentence

A **memory file** such as `AGENTS.md` or `CLAUDE.md` is a markdown file in your repo that the coding agent reads at the start of every session, so it knows your project's commands, conventions and rules without being told again.

## Why it matters in 2027

Agents start each session with an empty [context window](../00-foundations/tokens-and-context-windows.md). Without memory files, you re-explain the same things every day, and the agent repeats the same mistakes. A good memory file is the cheapest way to make an agent noticeably better on your codebase, and teams now review these files like any other code.

## Explain it like I'm new

A memory file is the note you leave for a substitute teacher: "Class starts at 9. Tests are in the blue folder. Never let Ravi near the chemicals." The substitute is capable but knows nothing about this class. A one-page note saves them from learning everything the hard way.

Where the analogy stops working: the agent treats the note as strong advice, not law. If something must never happen, enforce it with permissions or a [hook](subagents-and-hooks.md), not a sentence.

## How it works

Think of agent memory in two kinds:

| | Static memory | Dynamic memory |
|---|---|---|
| **What** | Files you write: `AGENTS.md`, `CLAUDE.md`, rules files | Notes the agent writes or loads as it works: auto memory, saved learnings, [skills](skills.md) loaded on demand |
| **When loaded** | Every session, automatically | When the agent decides it's relevant, or every session if small |
| **Good for** | Build and test commands, layout, conventions, "always/never" rules | Your preferences, corrections, procedures only some tasks need |
| **Risk** | Goes stale; too long and it gets ignored | Can store wrong or [poisoned](../06-agent-memory/memory-poisoning.md) lessons |

**`AGENTS.md`** is an open, tool-neutral format supported by most agents, including OpenAI Codex, Cursor, Google's tools and Claude Code. Claude Code also has its own `CLAUDE.md`, and can read `AGENTS.md` as well. Most agents also support:

- **Scopes.** A personal file in your home folder (applies to all projects), a project file in the repo (shared with the team), and files in subfolders (loaded when the agent works there).
- **Imports.** Pointing to other files instead of copying them in.

**Context engineering** is the wider skill: deciding what the agent sees. Memory files hold facts needed every session. Skills hold procedures needed sometimes. Everything else should be discovered by the agent reading the code.

## Example

A compact `AGENTS.md` for a Python service:

```markdown
# AGENTS.md

## Commands
- Install: `uv sync`
- Test: `uv run pytest -q` (must pass before you finish)
- Lint: `uv run ruff check . && uv run ruff format --check .`

## Layout
- `src/app/api/` HTTP handlers. Keep them thin; logic lives in `src/app/services/`.
- `tests/` mirrors `src/`.

## Rules
- Write a failing test before fixing a bug.
- Never edit files in `migrations/` by hand; run `uv run alembic revision`.
- Don't add dependencies without asking.
- Secrets come from environment variables. Never print or log them.
```

Every line is concrete and checkable. "Write clean code" would add nothing.

## Common mistakes

- **Writing an essay.** Long files waste context and dilute the rules that matter. Keep it to what you'd otherwise repeat.
- **Describing what the code already shows.** The agent can read the code. Write down what it can't discover: why decisions were made, commands, gotchas.
- **Never updating it.** When the agent makes the same mistake twice, add a line. When a rule stops being true, delete it.
- **Relying on it for security.** Instructions can be overridden by a clever prompt or injected text. Use permissions and hooks for hard rules.
- **Trusting memory files from strangers.** A malicious `AGENTS.md` in a cloned repo can instruct your agent to do harmful things. Read it before running an agent on unfamiliar code.

## Check yourself

1. What is the difference between static and dynamic memory for a coding agent?
2. Give two things that belong in `AGENTS.md` and one that doesn't.
3. Why is a memory file the wrong place to enforce "never push to main"?

<details>
<summary>Answers</summary>

1. Static memory is files you write that load every session. Dynamic memory is information the agent saves or loads as it works, such as auto-memory notes or skills.
2. Belong: the test command, a layout summary, a rule like "write a failing test first". Doesn't belong: a description of what each function does (the agent can read the code), or any secret.
3. The agent treats instructions as context, not as enforced configuration. A hard rule needs a permission setting, a hook, or branch protection on the Git server.

</details>

## Go deeper

- [AGENTS.md](https://agents.md) - The open format, with examples and the list of supporting tools. *Beginner · Website · 10 min*
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) - Clear explanation of instruction files versus auto memory. *Beginner · Docs · 15 min*
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md) by OpenAI - How Codex finds and layers these files. *Beginner · Docs · 10 min*
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) by Anthropic - The thinking behind what to put in context. *Intermediate · Article · 15 min*
