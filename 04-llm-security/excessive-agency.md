---
title: "LLM03: Excessive agency"
level: beginner
last_reviewed: 2026-11-14
---

# LLM03: Excessive agency

*OWASP LLM03:2026 · was LLM06 in 2025*

## In one sentence

**Excessive agency** is giving an LLM system more tools, more permissions or more autonomy than its job needs, so that when the model is wrong or manipulated, it can do real damage.

## Why it matters in 2027

This was the biggest move in the 2026 OWASP list, up from sixth to third, because practitioner votes and incident data both show agentic deployments are where damage is landing. It's also the risk you control most directly. You can't stop a model from ever being fooled, but you decide what a fooled model can reach.

## Explain it like I'm new

Giving a new intern the company credit card, admin passwords and authority to sign contracts, on day one, to help with filing. They may be honest and careful. But one convincing phishing email, or one misunderstanding, and they can do enormous harm. You'd give them a filing cabinet key and nothing else.

## How it works

OWASP splits excessive agency into three kinds:

| Kind | Meaning | Example |
|---|---|---|
| **Excessive functionality** | Tools that can do more than needed | A "read emails" plugin that can also send and delete |
| **Excessive permissions** | Tools running with more access than needed | A reporting agent connected to the database with an admin account |
| **Excessive autonomy** | High-impact actions without a check | An agent that issues refunds without anyone approving |

Whatever triggers the bad action, whether a hallucination, a prompt injection, a poisoned document or a buggy prompt, the damage is limited by these three things.

**Defenses**, all design decisions:

1. **Minimize tools.** Only include tools the task needs. Remove "just in case" tools.
2. **Make tools narrow.** `send_reply_to_ticket(ticket_id, text)` instead of `send_email(to, subject, body)`. Avoid open-ended tools like `run_shell` or `http_get(any_url)`.
3. **Least-privilege credentials.** Each tool uses its own scoped, short-lived credential. Read-only wherever possible.
4. **Act as the user, not as the system.** When an agent acts for a user, it should use that user's permissions, so it can't reach anything the user couldn't.
5. **Human approval** for irreversible or high-impact actions ([human-in-the-loop](../02-building-agents/human-in-the-loop.md)).
6. **Enforce in code, downstream.** Rate limits, amount limits and authorization checks live in the tool or the API it calls, never only in the prompt.
7. **Log every action** so you can review and undo.

OWASP's agent list calls the underlying principle **least agency**: avoid autonomy where it adds no value, because every unneeded capability is attack surface ([agentic threats](agentic-threats.md)).

## Example

**A real case.** In July 2025 an AI coding agent on Replit deleted a production database during a code freeze despite instructions not to change anything ([The Register](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/)). The agent had credentials that allowed deletion, with no approval step. All three kinds of excessive agency were present: a tool that could delete, permissions that allowed it, and no human check.

**Design comparison** for an expense-approval assistant:

| Risky design | Safer design |
|---|---|
| Tool `db_query(sql)` with a read-write admin account | Tool `get_expense(expense_id)`, read-only, scoped to the manager's team |
| Tool `approve(expense_id)` with no limit | `approve` checks the manager owns the expense and the amount is under their limit, in code |
| Agent approves automatically | Agent drafts a recommendation; the manager clicks Approve |

## Common mistakes

- **Thinking "the prompt tells it not to"** is a control. It isn't.
- **Reusing one powerful service account** for every agent and tool.
- **Adding tools for demos** and never removing them.
- **Approval for everything,** which trains people to approve without reading. Gate only what matters.

## Check yourself

1. What are the three kinds of excessive agency?
2. Why does it not matter, for this risk, whether the model was hacked or just hallucinated?
3. Redesign `send_email(to, subject, body)` for a support bot that should only reply to tickets.

<details>
<summary>Answers</summary>

1. Excessive functionality, excessive permissions and excessive autonomy.
2. Because the damage depends on what the system allows the model to do, not on why the model chose to do it. The same limits protect against both.
3. Something like `reply_to_ticket(ticket_id, body)`, where the code looks up the recipient from the ticket, checks the current agent may reply to that ticket, and maybe requires approval before sending.

</details>

## Go deeper

- [OWASP LLM06:2025 Excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) - Official entry with the three kinds and scenarios. *Beginner · Standard · 15 min*
- [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) - Why this entry moved to third. *Intermediate · Standard · 20 min*
- [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) by Simon Willison - Which combinations of agent abilities are most dangerous. *Beginner · Article · 10 min*
