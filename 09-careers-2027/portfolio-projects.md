---
title: Building a portfolio that gets interviews
level: beginner
last_reviewed: 2026-11-14
---

# Building a portfolio that gets interviews

## In one sentence

A strong AI engineering portfolio is three to five public projects that each solve a believable problem, include tests, evals and a threat model, and have a README that explains your decisions and what went wrong, so a reviewer can judge your thinking in five minutes.

## Why it matters in 2027

With coding agents, anyone can produce a working demo in an afternoon. Demos no longer stand out. What stands out is evidence of judgment: how you measured quality, what attacks you considered, what trade-offs you made, and what you'd do next. A small project with real evals beats a large one without them.

## Explain it like I'm new

An architect's portfolio doesn't just show pretty photos of buildings. It shows the brief, the site constraints, sketches, why they chose one design over another, and how the building performs. Hiring managers read your repos the same way.

## How it works

**Start from the five playbook projects, then make them yours.** Change the domain to something you care about, and extend one part significantly.

| Playbook project | Make it yours, for example |
|---|---|
| [P1](../projects/p1-agent-built-cli/README.md) agent-built CLI | A tool you actually use (expense splitting for your flat, a study planner), with your real agent mistakes in the reflection |
| [P2](../projects/p2-secure-rag/README.md) secure RAG | Your college's or city's public documents, with two user roles and permission tests |
| [P3](../projects/p3-langgraph-research-agent/README.md) research agent | A real search API, a critic node, and a SQLite checkpointer |
| [P4](../projects/p4-guardrailed-support-agent/README.md) support agent | Presidio or a classifier in place of regex, with before-and-after false-positive rates |
| [P5](../projects/p5-production-capstone/README.md) capstone | Deployed somewhere public, with a dashboard screenshot and a load test against a real model |

**A README reviewers love** has these sections:

1. **Problem and users** in two sentences.
2. **Architecture diagram.**
3. **How to run it** in under five commands, with no API key needed for tests.
4. **Results**: eval scores by category, latency, cost per task.
5. **Threat model**: a table of risks and controls.
6. **Decisions and trade-offs**: what you chose and why.
7. **What went wrong** and what you'd do next.

**Show your process.** A short "how I built this with a coding agent" section (what you delegated, what you checked, what the agent got wrong) is a strong signal in 2027, not a weakness.

**Write about one thing.** A short blog post or LinkedIn write-up explaining one finding ("Our injection filter blocked 12% of real questions; here's how I fixed it") is often what gets you noticed.

## Example

A results section that tells a reviewer a lot in a few lines:

```markdown
## Results (gemini-3.5-flash-lite, 60-case eval set)

| Category | Pass rate |
|---|---|
| Common questions | 93% |
| Hinglish | 81% (main gap: transliterated order IDs) |
| Out of scope | 100% |
| Injection and jailbreak | 100% |

p95 latency 2.8 s · ₹0.31 per conversation · input guardrail false-positive rate 3% (was 11% before the topic-check fix)
```

## Common mistakes

- **Ten tutorial clones.** Three original, well-tested projects are better.
- **No way to run it without paying.** Provide fake-model tests, as the playbook projects do.
- **Committing API keys.** Reviewers notice, and bots will find them.
- **Hiding failures.** Honest limitations read as maturity.

## Check yourself

1. Name the seven sections of a strong project README.
2. Why is a "what the agent got wrong" section a strength?
3. What's one quick way to make a playbook project yours?

<details>
<summary>Answers</summary>

1. Problem and users, architecture diagram, how to run it, results, threat model, decisions and trade-offs, what went wrong and next steps.
2. It shows you can direct and verify a coding agent, which is the skill employers want, rather than just accepting its output.
3. Change the domain to real data you care about and significantly extend one component, such as replacing regex guardrails with a classifier and measuring the difference.

</details>

## Go deeper

- [Skills checklist](skills-checklist.md) - What each project should prove. *Beginner · Note · 10 min*
- [Not all AI-assisted programming is vibe coding](https://simonwillison.net/2025/Mar/19/vibe-coding/) by Simon Willison - How to talk about building with AI responsibly. *Beginner · Article · 10 min*
- [Creating a LLM-as-a-Judge That Drives Business Results](https://hamel.dev/blog/posts/llm-judge/) by Hamel Husain - Ideas for a results section people trust. *Intermediate · Article · 30 min*
