---
title: Cost and latency
level: beginner
last_reviewed: 2026-11-14
---

# Cost and latency

## In one sentence

The cost of an LLM feature is mostly tokens multiplied by price per token, multiplied by the number of model calls per task, and its latency is mostly how many sequential calls you make and how many output tokens each one writes, so both are controlled by the same design choices.

## Why it matters in 2027

AI features that work in a demo often fail in production because each request costs too much or takes too long. Agents make this worse: one user question can trigger many calls. Engineers who can estimate cost per task, explain where latency comes from and cut both without hurting quality are in demand, and "how would you reduce cost?" is a standard interview question.

## Explain it like I'm new

A taxi ride. The fare depends on the distance (tokens) and the rate (price per token), and you pay for every leg if you change cars (each model call). How long it takes depends on how many legs you take one after another, and on traffic (output tokens are generated one at a time). A shorter route, fewer changes and a cheaper car for easy trips all help.

## How it works

**Cost per task:**

```text
cost = Σ over every model call ( input_tokens × input_price + output_tokens × output_price )
```

For agents, input tokens grow with each step, because every call resends the conversation so far.

**Latency per task:** time to first token, plus output tokens divided by generation speed, for each call, added up for calls that happen one after another.

**Ways to cut both:**

| Technique | Effect |
|---|---|
| **Use a smaller model** for easy steps (classification, routing, extraction) | Often 10× or more cheaper and faster |
| **Route by difficulty**: small model first, big model only when needed | Most traffic gets the cheap path |
| **Send fewer tokens**: retrieve fewer, better chunks; trim history | Lower input cost; often better answers |
| **Limit output**: `max_tokens`, ask for concise answers or JSON | Output is usually the most expensive and slowest part |
| **Prompt caching**: keep the long, unchanging part of the prompt identical at the start | Repeated prefixes are billed at a discount by many providers |
| **Response caching**: store answers to repeated questions | Repeats cost nothing |
| **Run independent calls in parallel** | Latency of the slowest, not the sum |
| **Fewer agent steps**: a [workflow](../02-building-agents/when-not-to-use-agents.md) instead of an open-ended agent | Fewer calls in total |
| **Stream the output** | Doesn't cut total time, but users see text sooner |
| **Batch APIs** for offline jobs | Many providers discount non-urgent requests |

**Measure first.** Record tokens, cost and latency per call and per feature ([observability](observability-and-tracing.md)). Report **p50 and p95** latency, not averages: the slowest 5% of requests are what users complain about.

## Example

A support bot answers 50,000 questions a day. Each answer takes two model calls (one to call a tool, one to write the reply). Assume 1,500 input and 150 output tokens per call, and illustrative prices of $0.10 per million input tokens and $0.40 per million output tokens (check your provider's [pricing page](https://ai.google.dev/gemini-api/docs/pricing) for real numbers).

```python
# test: run
calls_per_day = 50_000 * 2
input_cost = calls_per_day * 1_500 * 0.10 / 1e6
output_cost = calls_per_day * 150 * 0.40 / 1e6
print(f"per day: ${input_cost + output_cost:.2f}, per month: ${(input_cost + output_cost) * 30:,.0f}")
# per day: $21.00, per month: $630
```

Now suppose someone "improves" it by moving to a model with ten times the price, and by retrieving ten chunks instead of three, which takes input to 4,000 tokens. The monthly bill goes to roughly $14,000 for the same traffic. Measure before and after any change like that.

## Common mistakes

- **Using the biggest model for everything.**
- **Ignoring output length.** Verbose answers are slow and expensive.
- **Reporting average latency.** Use p95.
- **Forgetting agent loops.** Multiply by the real number of calls per task, measured from traces.
- **Breaking prompt caching** by putting changing content (timestamps, user names) at the start of the prompt.

## Check yourself

1. Why do agents get more expensive per step as they go?
2. Name three ways to cut cost without changing models.
3. Why report p95 latency rather than the average?

<details>
<summary>Answers</summary>

1. Each step resends the whole conversation so far, including earlier tool results, so input tokens grow.
2. Any three of: send fewer tokens, limit output length, prompt caching, response caching, fewer agent steps, batch APIs.
3. Averages hide the slow tail. The slowest requests are the ones users notice and complain about.

</details>

## Go deeper

- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) by Google - Real per-token prices, including caching and batch discounts. *Beginner · Docs · 10 min*
- [Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) by Anthropic - How caching works and how to structure prompts for it. *Intermediate · Docs · 15 min*
- [Context caching](https://ai.google.dev/gemini-api/docs/caching) by Google - The same idea in the Gemini API. *Intermediate · Docs · 10 min*
