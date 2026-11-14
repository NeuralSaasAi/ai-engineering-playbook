---
title: Threat modeling AI systems
level: intermediate
last_reviewed: 2026-11-14
---

# Threat modeling AI systems

## In one sentence

**Threat modeling** is a structured way to answer four questions about a system before attackers do: what are we building, what can go wrong, what are we going to do about it, and did we do a good enough job?

## Why it matters in 2027

AI systems add new ways to fail (injection, poisoning, excessive agency, memory attacks) on top of ordinary security problems. Security reviews, enterprise customers and regulators increasingly expect a written threat model for AI features. Being able to produce one quickly, using OWASP's AI lists, is a practical skill for both AI engineers and AI safety engineers.

## Explain it like I'm new

Before moving into a new flat, you walk through it asking: how could someone get in? Through the door, the balcony, a copied key from the old tenant? What's valuable? What would I do about each? Threat modeling is that walk-through, written down, for software.

## How it works

The four questions come from the [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/).

**1. What are we building?** Draw a data-flow diagram: users, components, data stores, external services, and **trust boundaries** (lines where data crosses from less trusted to more trusted, such as user input entering your app or a web page entering the model's context).

**2. What can go wrong?** Walk each element and each boundary-crossing with two checklists:

- **STRIDE** for classic threats: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege ([Microsoft](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)).
- **OWASP's AI lists** for AI-specific threats: the [LLM Top 10](../04-llm-security/README.md) and the [agentic Top 10](../04-llm-security/agentic-threats.md).

| Element in the diagram | Questions to ask |
|---|---|
| User input | Injection or jailbreak (LLM01)? Oversized input (LLM06)? |
| System prompt and context | Secrets or rules exposed (LLM08)? |
| Retrieved documents | Who can edit them (LLM05)? Tenant filtering (LLM09)? |
| Tools | More power than needed (LLM03)? Who checks arguments? |
| Model output | Rendered or executed unsafely (LLM10)? Wrong but trusted (LLM07)? |
| Memory | Can it be poisoned (ASI06)? Is it per user? |
| Other agents | Are messages authenticated (ASI07)? |
| Dependencies | Models, packages, MCP servers pinned and verified (LLM04)? |

**3. What are we going to do about it?** For each threat: mitigate, eliminate (remove the feature), transfer, or accept, and write down why. Prefer design controls over filters.

**4. Did we do a good enough job?** Turn each mitigation into a test: an eval case, a security test, a red-team scenario. Revisit the model when the design changes (a new tool, a new data source).

## Example

A threat model row from project [P5](../projects/p5-production-capstone/THREAT_MODEL.md):

| # | Threat | Where | Risk ID | Likelihood / impact | Decision | Verified by |
|---|---|---|---|---|---|---|
| T3 | A customer asks about another customer's order | `get_order_status` tool | LLM02, ASI03 | High / High | Mitigate: the tool checks ownership using the session's user ID; same "not found" reply for missing and foreign orders | `test_cannot_see_another_customers_order`; eval case `other-customers-order` |

Every row names a place in the diagram, a risk ID, a decision and a test. That's what makes a threat model useful instead of decorative.

## Common mistakes

- **Doing it once, after building.** Do a light version at design time and update it with each new tool or data source.
- **Listing threats without decisions.** Every row needs an owner and an outcome.
- **Ignoring non-AI threats.** Stolen API keys and weak authentication still cause most incidents.
- **Mitigations nobody tests.** Link each one to a test.

## Check yourself

1. What are the four threat-modeling questions?
2. What is a trust boundary? Give an AI-specific example.
3. What makes a threat-model row useful?

<details>
<summary>Answers</summary>

1. What are we building? What can go wrong? What are we going to do about it? Did we do a good enough job?
2. A line where data moves from less trusted to more trusted. For example, a retrieved web page entering the model's context, or model output going into a database query.
3. It names where the threat is, its risk ID, a decision, and a test that verifies the mitigation.

</details>

## Go deeper

- [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) - The four questions and core values, on one page. *Beginner · Website · 10 min*
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling) - Overview of methods and resources. *Beginner · Website · 15 min*
- [Multi-Agentic System Threat Modelling Guide](https://genai.owasp.org/resource/multi-agentic-system-threat-modeling-guide-v1-0/) by OWASP - Applying threat modeling to agent systems. *Intermediate · Guide · 45 min*
