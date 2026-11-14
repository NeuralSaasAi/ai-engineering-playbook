---
title: Agent skills and SKILL.md
level: beginner
last_reviewed: 2026-11-14
---

# Agent skills and SKILL.md

## In one sentence

A **skill** is a folder containing a `SKILL.md` file (plus optional scripts and reference files) that teaches an agent how to do one specific task, and the agent loads it only when a task needs it.

## Why it matters in 2027

Skills are how teams package "the way we do things here" (releasing, writing migrations, reviewing security, generating reports) so every agent does it the same way. The format is an open standard that many agents support, so one skill can work across Claude Code, OpenAI Codex, Cursor, Google's agents and others. Writing good skills is quickly becoming a normal part of an engineer's job.

## Explain it like I'm new

A skill is a recipe card in a kitchen drawer. The chef doesn't memorize every recipe, and doesn't read the whole cookbook before each meal. The drawer has labeled cards ("sourdough", "biryani"), and when someone orders biryani the chef pulls out that card. The label is short, so scanning the drawer is quick. The card can include detailed steps and even tools (scripts) to use.

Where the analogy stops working: the chef decides which card to pull based only on the label. A vague label means the right skill never gets used.

## How it works

```text
.agents/skills/release-notes/       (location varies by tool, e.g. .claude/skills/)
├── SKILL.md            # required: name, description, instructions
├── template.md         # optional: reference material
└── scripts/
    └── changelog.py    # optional: code the agent can run
```

`SKILL.md` starts with front matter. At minimum it has a `name` and a `description`:

```markdown
---
name: release-notes
description: Write release notes from merged pull requests. Use when the user asks for release notes, a changelog, or a summary of what shipped.
---
```

Loading happens in stages, which is called **progressive disclosure**:

1. At startup, the agent sees only each skill's name and description (a few dozen tokens each).
2. When a task matches a description, the agent reads the full `SKILL.md`.
3. If the instructions point to other files or scripts, it opens or runs them only when needed.

This means you can install many skills without filling the [context window](../00-foundations/tokens-and-context-windows.md).

**Skills vs the other features:**

| Use | When |
|---|---|
| [Memory file](context-and-memory-files.md) | Facts needed in every session |
| Skill | A procedure needed for some tasks |
| [MCP server](mcp.md) | Live access to an outside system (an API, a database) |
| [Hook](subagents-and-hooks.md) | Something that must always happen, enforced by code |

## Example

A complete small skill:

```markdown
---
name: add-api-endpoint
description: Add a new HTTP endpoint to this FastAPI service, with validation and tests. Use when asked to add or expose a new API route.
---

# Adding an endpoint

1. Define request and response models in `src/app/schemas/` using Pydantic.
2. Put business logic in `src/app/services/`, never in the route handler.
3. Add the route in `src/app/api/`, with an explicit `response_model`.
4. Write tests in `tests/api/` covering: success, validation error (422), and unauthorized (401).
5. Run `uv run pytest -q tests/api` and fix failures before finishing.
6. Add the endpoint to `docs/api.md`.

Never return database objects directly. Never log request bodies (they may contain personal data).
```

Project [P1](../projects/p1-agent-built-cli/README.md) includes a real skill you can try.

## Common mistakes

- **Vague descriptions.** "Helps with APIs" won't trigger reliably. Say what it does and when to use it, using words a user would actually type.
- **One giant skill.** Split by task. Small, focused skills load faster and get picked correctly.
- **Putting secrets in skills.** Skill files are plain text that the model reads. Use environment variables.
- **Installing skills you haven't read.** A skill can contain scripts and instructions that run with your permissions. Treat third-party skills like third-party code (see [supply chain](../04-llm-security/supply-chain.md)).

## Check yourself

1. What are the two required fields in a skill's front matter?
2. What is progressive disclosure, and why does it matter?
3. Your team has a 12-step release process. Memory file, skill, or hook?

<details>
<summary>Answers</summary>

1. `name` and `description`.
2. The agent loads only skill names and descriptions at first, then the full instructions and files only when needed. It keeps the context window small even with many skills installed.
3. A skill. It's a procedure needed only for some tasks. (If one step must never be skipped, also enforce it with a hook or CI check.)

</details>

## Go deeper

- [Agent Skills overview](https://agentskills.io/home) - The open standard, and which tools support it. *Beginner · Docs · 10 min*
- [Agent Skills specification](https://agentskills.io/specification) - Every front matter field and folder rule. *Intermediate · Spec · 15 min*
- [Skills in Claude Code](https://code.claude.com/docs/en/skills) - Creating, testing and sharing skills. *Beginner · Docs · 15 min*
- [Skills in Codex](https://developers.openai.com/codex/skills) by OpenAI - The same format as used by Codex. *Beginner · Docs · 10 min*
