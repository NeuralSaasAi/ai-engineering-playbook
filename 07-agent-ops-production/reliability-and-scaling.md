---
title: Reliability and scaling
level: intermediate
last_reviewed: 2026-11-14
---

# Reliability and scaling

## In one sentence

**Reliability** for AI apps means the system keeps giving acceptable answers when providers are slow, rate-limited or down, when traffic spikes, and when a step fails, using timeouts, retries, fallbacks, limits and graceful degradation.

## Why it matters in 2027

LLM providers have outages and rate limits, responses take seconds instead of milliseconds, and agents chain many fallible steps. A demo that "falls over under load" isn't a product. Knowing how to load test, set limits and fail gracefully is what separates a prototype from something a company can depend on.

## Explain it like I'm new

A restaurant on a festival night. A good one doesn't collapse when 200 people arrive. It takes bookings (rate limits), has a shorter menu ready for rush hour (degraded mode), calls a second supplier if the first one doesn't deliver (fallback), and tells customers honestly how long the wait is instead of leaving them guessing.

## How it works

| Problem | Pattern |
|---|---|
| A provider call hangs | **Timeouts** on every call, shorter than your users' patience |
| Temporary errors (429, 500, 503) | **Retries** with exponential backoff and jitter, capped at a few attempts |
| A provider is down or overloaded | **Fallback** to another model or provider, configured in advance ([gateways](../03-ai-safety-guardrails/llm-gateways.md)) |
| Repeated failures | **Circuit breaker**: stop calling a failing dependency for a short time instead of piling on |
| Traffic spikes, abuse | **Rate limits** and **quotas** per user and tenant ([unbounded consumption](../04-llm-security/unbounded-consumption.md)) |
| Too much load | **Queues** for work that doesn't need an instant answer; **load shedding** for the rest |
| Agent loops or long tasks | **Step and time budgets**; checkpoints so work can resume ([LangGraph](../02-building-agents/langgraph-basics.md)) |
| Everything is slow | **Graceful degradation**: a smaller model, cached answers, or "we'll email you" |

**Scaling the app itself.** Keep the web layer stateless so you can run more copies behind a load balancer. Put shared state (rate-limit counters, conversation checkpoints, caches) in a shared store such as Redis or Postgres. In-memory state only works with one process.

**Load testing.** Before launch, send realistic traffic (a mix of normal questions and attacks) at the expected peak and above. Watch p95 latency, error rates, 429s, and cost. Tools: [Locust](https://docs.locust.io/) (Python) or [k6](https://grafana.com/docs/k6/latest/). Use a fake or cheap model for most load tests, so you test your system rather than paying to test the provider.

**Define what "working" means.** Pick a few service-level objectives, such as "95% of answers within 4 seconds" and "99.5% of requests don't error", and alert when you're burning through them.

## Example

Project [P5](../projects/p5-production-capstone/README.md) includes a load test that mixes normal traffic with attacks:

```text
$ uv run capstone-load
requests:     45 in 0.06s (716 req/s)
status codes: {200: 30, 429: 15}
latency ms:   p50=3.5  p95=6.8  max=50.7
server cost:  $0.000918 (estimated)
```

The 429s are the rate limiter doing its job: three demo users each sent 15 requests, with a limit of 10 per minute. With the fake model, latency shows your code's overhead. Run it again with `LIVE=1` to see what a real provider adds.

## Common mistakes

- **No timeouts.** One stuck request ties up a worker forever.
- **Retrying everything.** Don't retry 400 errors, and don't retry so fast that you make an outage worse.
- **Fallback to a model you've never evaluated.** Run your evals against the fallback model too.
- **Rate limits held in memory** with several server processes. Each process counts separately.
- **Load testing only the happy path.** Include long inputs, attacks and tool-heavy questions.

## Check yourself

1. What's the difference between a retry and a fallback?
2. Why must rate-limit counters live in a shared store once you run more than one server process?
3. Why run load tests mostly against a fake model?

<details>
<summary>Answers</summary>

1. A retry tries the same call again after a temporary error. A fallback switches to a different model or provider.
2. Each process would otherwise keep its own count, so a user could get N times the intended limit.
3. To measure your own system's behavior (limits, queues, overhead) cheaply and repeatably, without paying for or being limited by the provider.

</details>

## Go deeper

- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) by Google - Free book; read the chapters on SLOs and handling overload. *Intermediate · Book · browse*
- [Locust documentation](https://docs.locust.io/) - Load testing in Python. *Beginner · Docs · 20 min*
- [LiteLLM proxy](https://docs.litellm.ai/docs/simple_proxy) - Retries, fallbacks and limits at the gateway. *Intermediate · Docs · 20 min*
