# Design doc: shop support agent v1

Status: implemented in P4 and P5 · Last updated 2026-11-14 · Uses the seven steps from [AI system design fundamentals](../../08-ai-system-design/design-fundamentals.md).

## 1. Problem and users

An online shop's support team spends most of its time on three questions: "where is my order?", "what's the return policy?" and "I want a refund". Customers write in English, Hindi and Hinglish. We want an assistant that resolves the first two on its own and prepares the third for a human.

**If it's wrong:** customers get bad information, wrongful refunds or leaked data, and screenshots go public. So the assistant drafts and looks things up; it never moves money.

## 2. Targets

| Metric | Target | How measured |
|---|---|---|
| Correct and on-policy answers | ≥ 90% overall, 100% on security cases | Eval suite in CI |
| p95 latency | < 4 s | Traces |
| Cost | < ₹0.50 per conversation | Gateway usage metrics |
| Cross-customer leaks | 0 | Security evals + red-team scans |
| Availability | 99.5% of requests without server error | Metrics and alerts |

## 3. Shape

One agent, two tools, at most four model calls per message. A multi-agent design adds cost and failure points without improving these three tasks. A fixed workflow almost works, but the agent's choice between "look up", "explain" and "open a ticket" is cheaper to maintain than a hand-written router.

## 4. Data path

- Order data only through `get_order_status`, filtered by the session's user ID.
- Return policy is short and stable, so it's in the prompt for v1. Move to RAG with citations when the policy grows.
- No conversation memory across sessions in v1 (avoids memory poisoning and privacy work until there's a clear need).

## 5. Action path

| Tool | Can do | Can't do | Approval |
|---|---|---|---|
| `get_order_status` | Read status of the user's own orders | See other users' orders | None |
| `request_refund` | Create a ticket with a reason | Move money, approve anything | Human review of every ticket |

## 6. Safety layers

Auth (token to user ID) → gateway (10 requests per minute per user, 20,000 tokens per day) → input guards (size, injection, topic, PII masking) → agent → output guards (PII, commitments, link allowlist). See [THREAT_MODEL.md](THREAT_MODEL.md).

## 7. Measurement and operations

- **Before release:** 12-case tagged eval set with a rule judge in CI; a live LLM judge on demand, calibrated against human labels.
- **After release:** OpenTelemetry traces (no message text), `/metrics` for cost and latency percentiles, alerts on error rate, p95 latency, cost per hour and guardrail block rate.
- **Load:** `capstone-load` before each release; with real models, at the expected peak.
- **Deploy:** container built from the lockfile, non-root, health check; rollout from CI only.

## Trade-offs we chose

| Decision | Alternative | Why |
|---|---|---|
| Regex and checksum guardrails | Classifier models | Fast, transparent, testable for v1. Plan: add a classifier and compare false-positive rates |
| Policy in prompt | RAG | Policy is half a page. RAG adds moving parts for no gain yet |
| No refund tool | Refund tool with limits | Removes the worst failure entirely. Humans already review refunds |
| In-process rate limiter | Redis or a gateway | Fine for one process. Must change before scaling out (see open items) |
| Gemini Flash-Lite default | Larger model | Meets eval targets at much lower cost; switch per environment via `MODEL` |

## Open questions

- Should conversations be kept for quality review, and for how long, under DPDP? Proposed: 30 days, masked, access-logged.
- Do we add WhatsApp as a channel? It would need a new threat-model pass (identity, media messages).
