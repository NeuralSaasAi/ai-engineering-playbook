---
title: "LLM06: Unbounded consumption"
level: beginner
last_reviewed: 2026-11-14
---

# LLM06: Unbounded consumption

*OWASP LLM06:2026 · was LLM10 in 2025*

## In one sentence

**Unbounded consumption** is when an LLM app has no effective limits on how much it can be used, so attackers (or bugs) can run up huge bills, slow or crash the service, or copy the model's behavior by querying it at scale.

## Why it matters in 2027

LLM calls are expensive compared with normal web requests, and the attacker pays almost nothing to trigger them. OWASP calls this **cost asymmetry**. Reasoning models that "think" for thousands of tokens, and agents that loop through many calls per request, make it worse. This risk rose four places in the 2026 list. It's also the risk most likely to hit a beginner's side project, through a leaked API key.

## Explain it like I'm new

An all-you-can-eat buffet with no time limit and no limit on takeaway boxes. Most diners are fine. One person brings 50 boxes, or 200 friends, and the restaurant goes broke by lunchtime.

## How it works

| Attack or failure | What happens |
|---|---|
| **Denial of wallet** | Floods of expensive requests (long inputs, long outputs, reasoning-heavy prompts) drive up your bill |
| **Denial of service** | Requests consume your rate limit or capacity, so real users get errors |
| **Agent loops** | A confused or manipulated agent calls tools and the model again and again |
| **Stolen keys** | A leaked API key is used by others until you notice |
| **Model extraction** | Mass querying to copy a model's behavior, or even recover parts of it ([Carlini et al., 2024](https://arxiv.org/abs/2403.06634)) |

**Defenses:**

- **Rate limits** per user, per API key and per IP, on requests *and* tokens.
- **Size limits**: maximum input length, `max_tokens` on every call, and caps on reasoning effort where the provider supports it.
- **Agent budgets**: maximum steps, tool calls, tokens and time per task ([the agent loop](../02-building-agents/the-agent-loop.md)).
- **Spending caps and alerts** at the provider level. Set them on day one.
- **Authentication** for anything that triggers model calls. No anonymous endpoints that call paid APIs.
- **Caching** repeated questions so they don't cost twice.
- **Keep keys out of front-end code and Git.** Rotate any key that was ever exposed.
- **Monitor** cost per user and per feature, and alert on spikes ([cost and latency](../07-agent-ops-production/cost-and-latency.md)).

An [LLM gateway](../03-ai-safety-guardrails/llm-gateways.md) is a common place to enforce most of these in one spot. Project [P4](../projects/p4-guardrailed-support-agent/README.md) implements per-user rate limits and budgets.

## Example

A student builds a "chat with your PDF" app and puts the API key in the JavaScript sent to the browser. Someone copies the key from the page source and uses it for their own projects. By the end of the month the bill is many times the student's budget.

What would have prevented it, cheapest first:

1. Keep the key on a server; the browser calls your server, not the provider.
2. Set a monthly spending cap and email alerts in the provider console.
3. Require login, and rate-limit each user.

## Common mistakes

- **No `max_tokens`** on calls, so one request can produce a very long, expensive output.
- **Rate-limiting requests but not tokens.** One huge request can cost more than a thousand small ones.
- **No step limit on agents.**
- **Discovering the problem from the invoice.** Set alerts.

## Check yourself

1. What does cost asymmetry mean for LLM apps?
2. Why should you rate-limit tokens, not only requests?
3. Name three settings you should configure on day one of any LLM project.

<details>
<summary>Answers</summary>

1. An attacker can trigger expensive computation at almost no cost to themselves, while you pay for every token.
2. Requests vary hugely in size. A few very large requests can cost as much as thousands of small ones, while staying under a request-count limit.
3. Any three of: a provider spending cap with alerts, `max_tokens` on every call, per-user rate limits, step limits for agents, and keeping keys server-side.

</details>

## Go deeper

- [OWASP LLM10:2025 Unbounded consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) - Official entry. *Beginner · Standard · 15 min*
- [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) by Google - How providers count requests and tokens. *Beginner · Docs · 5 min*
- [Stealing Part of a Production Language Model](https://arxiv.org/abs/2403.06634) - Why mass querying can be a theft risk. *Intermediate · Paper · 30 min*
