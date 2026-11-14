---
title: Skills checklist
level: beginner
last_reviewed: 2026-11-14
---

# Skills checklist

## In one sentence

This skills checklist lists what a beginner-to-intermediate AI engineer should be able to *do* (not just know) by the end of this playbook, grouped by module, so you can tick off what you've proven and see what's left.

## Why it matters in 2027

"I watched a course" isn't evidence. "I built this, tested it this way, and here's what broke" is. A checklist of concrete, demonstrable skills keeps your learning honest and gives you material for your CV, portfolio and interviews.

## Explain it like I'm new

A driving licence test has a list: start on a hill, reverse park, emergency stop. You don't pass by explaining them. You pass by doing each one in front of an examiner. Treat each line below the same way, and only tick it when you've done it and can show it.

## How it works

Copy this into your own notes or a GitHub issue and tick as you go. Each line links to where it's taught.

**Foundations**

- [ ] Explain tokens, context windows, temperature and why LLMs hallucinate ([00](../00-foundations/README.md))
- [ ] Call an LLM from Python with retries, timeouts and token logging ([calling an API](../00-foundations/calling-an-llm-api.md))
- [ ] Build a small RAG pipeline and explain each step ([RAG](../00-foundations/rag-in-one-page.md))

**Coding agents**

- [ ] Use one coding agent daily, following plan, tests, implement, review ([workflow](../01-coding-agents/agentic-sdlc.md))
- [ ] Write an `AGENTS.md` and a skill for a real project ([P1](../projects/p1-agent-built-cli/README.md))
- [ ] Connect an MCP server with a least-privilege token ([MCP](../01-coding-agents/mcp.md))
- [ ] Keep a log of agent mistakes and the rules you added because of them

**Building agents**

- [ ] Design narrow tools with permission checks in code ([tool calling](../02-building-agents/tool-calling.md))
- [ ] Build a LangGraph agent with a checkpointer and a human approval step ([P3](../projects/p3-langgraph-research-agent/README.md))
- [ ] Argue when *not* to use an agent ([when not to](../02-building-agents/when-not-to-use-agents.md))

**Safety and security**

- [ ] Explain every OWASP LLM Top 10 (2026) risk with an example and a defense ([04](../04-llm-security/README.md))
- [ ] Explain the OWASP agentic risks and "least agency" ([agentic threats](../04-llm-security/agentic-threats.md))
- [ ] Demonstrate an indirect prompt injection and stop it with design controls ([P2](../projects/p2-secure-rag/README.md))
- [ ] Build input, output and action guardrails and measure their false positives ([P4](../projects/p4-guardrailed-support-agent/README.md))
- [ ] Mask Indian PII formats with checksums ([PII](../03-ai-safety-guardrails/pii-and-privacy.md))

**Evaluation**

- [ ] Build a 30-case golden dataset with tags, including adversarial cases ([datasets](../05-evaluation/golden-datasets.md))
- [ ] Write an LLM-as-judge rubric and check it against your own labels ([judge](../05-evaluation/llm-as-judge.md))
- [ ] Run an automated red-team scan and turn findings into tests ([red-teaming](../05-evaluation/red-teaming.md))

**Memory, production and design**

- [ ] Design memory writes that resist poisoning and respect deletion ([06](../06-agent-memory/README.md))
- [ ] Trace an agent end to end with OpenTelemetry, without logging personal data ([tracing](../07-agent-ops-production/observability-and-tracing.md))
- [ ] Estimate cost per task and cut it by half without losing quality ([cost](../07-agent-ops-production/cost-and-latency.md))
- [ ] Load test an AI endpoint and explain the results ([P5](../projects/p5-production-capstone/README.md))
- [ ] Write a design doc and a threat model for an AI feature ([08](../08-ai-system-design/README.md))
- [ ] Explain what DPDP and the EU AI Act mean for a design ([compliance](../08-ai-system-design/compliance-basics.md))

## Example

Turning a ticked line into CV evidence:

> **Built a guardrailed support agent** (Python, LiteLLM, FastAPI). Input, output and action guardrails mapped to OWASP LLM Top 10 2026; Luhn/Verhoeff-checked PII masking for Indian formats; per-user rate limits and token budgets. Eval suite of 12 tagged cases with an LLM-as-judge, gating CI at 100% on security cases.

Specific, checkable, and every claim links to code.

## Common mistakes

- **Ticking items you've only read about.**
- **Skipping the "measure it" parts** (evals, false-positive rates, cost). They're what employers notice.
- **Doing everything in tutorials' happy paths.** Break things on purpose.

## Check yourself

1. What's the test for ticking a line on this list?
2. Which three items would best show security skill?
3. What makes a CV line like the example convincing?

<details>
<summary>Answers</summary>

1. You've done it yourself and can show the result (code, a write-up, numbers).
2. Any three of the safety and security items, especially the injection demo with design controls, guardrails with measured false positives, and a threat model.
3. It names specific techniques and numbers, maps to a recognized standard, and every claim can be checked in the code.

</details>

## Go deeper

- [Portfolio projects](portfolio-projects.md) - Turning skills into public evidence. *Beginner · Note · 10 min*
- [90-day plan](90-day-plan.md) - A schedule that covers this whole list. *Beginner · Note · 10 min*
- [Your AI product needs evals](https://hamel.dev/blog/posts/evals/) by Hamel Husain - Why measurement skills stand out. *Beginner · Article · 25 min*
