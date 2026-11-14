---
title: A 90-day plan for 2027
level: beginner
last_reviewed: 2026-11-14
---

# A 90-day plan for 2027

## In one sentence

This 90-day plan works through the whole playbook in about 8 to 10 hours a week: four weeks on foundations, coding agents and building agents, four weeks on safety, security and evaluation, and four to five weeks on memory, production, system design and your portfolio.

## Why it matters in 2027

A plan turns "I should learn AI safety" into "this week I break and fix a RAG app". The order matters: you need to build before you can secure, and secure before you can design for production. Most people who stall do so because they skip the building or never start the measuring.

## Explain it like I'm new

Training for a 10 km run. You don't run 10 km on day one. You follow a schedule: short runs, then longer ones, a rest week, then a timed run at the end. Each week has a clear target, and you can see progress.

## How it works

**Month 1: build** (weeks 1 to 4)

| Week | Do | Done when |
|---|---|---|
| 1 | [00 · Foundations](../00-foundations/README.md); make your first API call | You can explain RAG and token cost to a friend |
| 2 | [01 · Coding agents](../01-coding-agents/README.md); set up one agent; write an `AGENTS.md` | Your agent follows your project rules |
| 3 | Build [P1](../projects/p1-agent-built-cli/README.md) from the spec with your agent | Tests pass; reflection written |
| 4 | [02 · Building agents](../02-building-agents/README.md); run every snippet | You've built a LangGraph graph with an approval step |

**Month 2: secure and measure** (weeks 5 to 8)

| Week | Do | Done when |
|---|---|---|
| 5 | [04 · LLM security](../04-llm-security/README.md), first half; play Gandalf | You can explain LLM01 to LLM05 with examples |
| 6 | Finish module 04; build and attack [P2](../projects/p2-secure-rag/README.md) | You've added one new attack and fixed it |
| 7 | [03 · Guardrails](../03-ai-safety-guardrails/README.md) and [05 · Evaluation](../05-evaluation/README.md) | You've built a 30-case eval set for P2 |
| 8 | Build [P4](../projects/p4-guardrailed-support-agent/README.md); swap in one real guardrail library | You've measured its false-positive rate |

**Month 3: production and portfolio** (weeks 9 to 13)

| Week | Do | Done when |
|---|---|---|
| 9 | [06 · Memory](../06-agent-memory/README.md); build [P3](../projects/p3-langgraph-research-agent/README.md) | Memory carries across sessions, safely |
| 10 | [07 · Agent ops](../07-agent-ops-production/README.md); run [P5](../projects/p5-production-capstone/README.md) with Docker and Jaeger | You've read a trace and a load-test report |
| 11 | [08 · System design](../08-ai-system-design/README.md); write a design doc for your own idea | Design doc and threat model done |
| 12 | Turn two projects into portfolio pieces ([portfolio](portfolio-projects.md)) | READMEs with results and threat models |
| 13 | Write one public post; practice two design questions out loud | Post published; mock interviews done |

**Weekly rhythm** (8 to 10 hours): two evenings reading and doing the "Check yourself" questions, one long session building, and 30 minutes updating your [skills checklist](skills-checklist.md) and agent-mistakes log.

**If you have less time**, stretch to 26 weeks and keep the same order. **If you already build with LLMs**, skip to week 5 and do P1 as a quick warm-up.

## Example

A realistic week 6:

- **Mon (1 h):** read [vector weaknesses](../04-llm-security/vector-and-embedding-weaknesses.md) and [improper output handling](../04-llm-security/improper-output-handling.md).
- **Wed (1.5 h):** run `secure-rag attack`; turn off one defense at a time and note which attacks return.
- **Sat (4 h):** write a Markdown-link exfiltration attack; watch it get through; fix the sanitizer; add tests.
- **Sun (30 min):** tick the checklist; write three sentences on what surprised you.

## Common mistakes

- **Reading every link before building anything.** Build every week.
- **Skipping month 2** to get to "cool" agent work. Security and evals are what employers are hiring for.
- **No public output.** Write up at least one thing.
- **Giving up after a missed week.** Shift the plan, don't drop it.

## Check yourself

1. Why does building come before securing in this plan?
2. What's the "done when" for week 8?
3. What should you change if you already build LLM apps?

<details>
<summary>Answers</summary>

1. You need to understand how the parts work, and have something to attack, before you can defend it well.
2. You've swapped one guardrail for a real library in P4 and measured its false-positive rate.
3. Start at week 5, doing P1 quickly as a warm-up for the agent workflow.

</details>

## Go deeper

- [Skills checklist](skills-checklist.md) - Track what you've proven. *Beginner · Note · 10 min*
- [Gandalf](https://gandalf.lakera.ai/) by Lakera - A fun week-5 warm-up for prompt injection. *Beginner · Interactive · 30 min*
- [LangChain Academy: Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) - Extra practice for week 4. *Beginner · Course · 6 h*
