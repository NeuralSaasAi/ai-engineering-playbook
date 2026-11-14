---
title: Choosing a coding agent
level: beginner
last_reviewed: 2026-11-14
---

# Choosing a coding agent

## In one sentence

The main **coding agents** in late 2026 (Claude Code, OpenAI Codex, Google Antigravity, and editor-based tools such as Cursor, GitHub Copilot and Kiro) share the same core features, so pick one that fits your budget and workflow, learn it well, and the skills will transfer.

## Why it matters in 2027

Employers care less about which agent you use than about whether you use one well. But prices, free tiers and product names change every few months. For example, Google stopped serving its Gemini CLI to free and individual subscribers on 18 June 2026 and moved them to the Antigravity CLI ([announcement](https://github.com/google-gemini/gemini-cli/discussions/27274)). Knowing the field helps you start cheaply and avoid being stranded.

## Explain it like I'm new

Choosing between Android phones. They all make calls, run apps and take photos. The differences are in the details, the price and which ecosystem you already live in. Spending a week getting really good with one teaches you most of what you need for the others.

## How it works

Comparison as of **14 November 2026**. Prices are USD per month for individuals, before tax. Check the linked pricing pages, because these change often.

| Agent | Where it runs | Entry price | Notable for | Pricing page |
|---|---|---|---|---|
| **Claude Code** (Anthropic) | Terminal, IDE extensions, desktop, web | Included with Claude Pro, $20 ($17 billed yearly). Higher tiers from $100 | Skills, subagents, hooks, plan mode, auto memory | [claude.com/pricing](https://claude.com/pricing) |
| **OpenAI Codex** | Terminal (CLI), IDE extension, cloud tasks | Included with ChatGPT Plus, $20. Pro tiers from $100 | Sandboxed by default, `AGENTS.md`, cloud tasks that open pull requests | [Codex pricing](https://developers.openai.com/codex/pricing) |
| **Google Antigravity** | Desktop app, CLI (`agy`) | Free individual tier with rate limits. More quota through Google AI plans | Agent manager for parallel agents, browser control, Gemini models | [antigravity.google/pricing](https://antigravity.google/pricing) |
| **Cursor** | Its own editor (VS Code-based) | Free tier; paid plans | Tight editor integration, many model choices | [cursor.com/pricing](https://cursor.com/pricing) |
| **GitHub Copilot** | VS Code, JetBrains, GitHub.com | Free tier; paid plans | Built into GitHub, coding agent that works from issues | [Copilot plans](https://github.com/features/copilot/plans) |
| **Kiro** (AWS) | Its own editor (VS Code-based), CLI | Free tier; paid plans | Spec-driven development, hooks, steering files | [kiro.dev/pricing](https://kiro.dev/pricing/) |

What they have in common, and what this module teaches:

- An [agent loop](../02-building-agents/the-agent-loop.md) that reads, edits, runs and verifies.
- [Memory files](context-and-memory-files.md) (`AGENTS.md` or a tool-specific equivalent).
- [Skills](skills.md) in the open `SKILL.md` format, or something very close.
- [MCP](mcp.md) for connecting outside tools.
- Permission modes, and often [subagents and hooks](subagents-and-hooks.md).

**How to choose:**

1. **Budget zero?** Start with a free tier (Antigravity, Copilot Free, Cursor or Kiro free plans). Expect rate limits.
2. **Already paying for ChatGPT or Claude?** Use the agent included in that plan.
3. **Prefer the terminal?** Claude Code, Codex CLI or the Antigravity CLI. **Prefer an editor?** Cursor, Copilot, Kiro or Antigravity.
4. **At work?** Use what your company has approved. Enterprise plans add data-retention and admin controls that matter for client code.

A $20 plan is enough to learn on. Upgrade only when you're hitting limits on real work.

## Example

A one-week plan to get properly good at one agent:

| Day | Do this |
|---|---|
| 1 | Install it. Ask it to explain an open-source repo you know. Don't let it edit. |
| 2 | Write an `AGENTS.md` for one of your projects. Watch which rules it follows. |
| 3 | Fix a real bug using the [agentic workflow](agentic-sdlc.md): plan, failing test, fix, review. |
| 4 | Write one [skill](skills.md) for a task you repeat. |
| 5 | Connect one [MCP server](mcp.md) (GitHub or a database), with a read-only token. |
| 6 | Add one hook or permission rule that blocks something dangerous. |
| 7 | Build [project P1](../projects/p1-agent-built-cli/README.md) end to end. |

## Common mistakes

- **Tool-hopping.** Switching every week means you never learn any of them deeply.
- **Paying for the top tier first.** Learn on an entry plan; upgrade when you hit real limits.
- **Using a personal plan for client code** without checking your employer's policy on data and IP.
- **Trusting old blog posts.** This field changes monthly. Check the official pricing and docs pages.

## Check yourself

1. Which five features do almost all coding agents share?
2. What happened to Gemini CLI for individual users in June 2026?
3. Why should you check official pricing pages instead of comparison blogs?

<details>
<summary>Answers</summary>

1. The agent loop, memory files, skills, MCP connections, and permission controls (often with subagents and hooks).
2. Google stopped serving it for free and Google AI Pro/Ultra users on 18 June 2026 and pointed them to the Antigravity CLI.
3. Prices, limits and plan names change every few months, so third-party summaries go out of date quickly.

</details>

## Go deeper

- [Claude Code overview](https://code.claude.com/docs/en/overview) - Install and first steps. *Beginner · Docs · 10 min*
- [OpenAI Codex](https://developers.openai.com/codex) - Install and first steps. *Beginner · Docs · 10 min*
- [Google Antigravity docs](https://antigravity.google/docs) - Install and first steps. *Beginner · Docs · 10 min*
- [Kiro docs](https://kiro.dev/docs/specs/) - Spec-driven workflow. *Beginner · Docs · 10 min*
