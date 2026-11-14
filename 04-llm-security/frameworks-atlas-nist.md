---
title: "Frameworks: MITRE ATLAS and NIST AI RMF"
level: intermediate
last_reviewed: 2026-11-14
---

# Frameworks: MITRE ATLAS and NIST AI RMF

## In one sentence

**MITRE ATLAS** is a public catalog of real attacker tactics and techniques against AI systems, and the **NIST AI Risk Management Framework** (AI RMF) is a voluntary guide for organizations to govern, map, measure and manage AI risks; together with OWASP, they're the three references you'll meet most in AI security work.

## Why it matters in 2027

Security teams speak in framework IDs. A threat model, audit or vendor questionnaire will ask how your system maps to OWASP, ATLAS or NIST. OWASP's 2026 LLM list itself includes mappings to ATLAS, NIST and other frameworks. You don't need to memorize them, but you should know what each is for and how to look things up.

## Explain it like I'm new

Three reference books on a security engineer's desk:

- **OWASP Top 10**: "the ten most common ways apps like yours get broken". A checklist for builders.
- **MITRE ATLAS**: "the attacker's playbook", a detailed catalog of how real attacks unfold, step by step. For threat modeling and red teams.
- **NIST AI RMF**: "how an organization manages AI risk overall", covering policies, roles, measurement and response. For leadership and compliance.

## How it works

| | OWASP LLM and Agentic Top 10 | MITRE ATLAS | NIST AI RMF |
|---|---|---|---|
| **Made by** | OWASP GenAI Security Project (community) | MITRE (non-profit, US) | US National Institute of Standards and Technology |
| **Shape** | Ranked lists of risks with mitigations | A matrix of tactics (goals) and techniques (methods), plus case studies | Four functions: Govern, Map, Measure, Manage |
| **Use it to** | Review a design or code; prioritize fixes | Model how an attacker would chain steps; plan red-team exercises | Set up organization-wide AI risk processes |
| **Modeled on** | OWASP Top 10 for web apps | MITRE ATT&CK for traditional cyberattacks | NIST Cybersecurity Framework |

**MITRE ATLAS** organizes attacks like ATT&CK does: tactics are the attacker's goals (reconnaissance, initial access, exfiltration, impact) and techniques are how they do it (for example, LLM prompt injection or poisoning training data). Each technique has an ID, so a red-team report can say exactly what was tested. ATLAS also publishes case studies of real attacks.

**NIST AI RMF 1.0** (January 2023) is voluntary and not specific to any technology:

- **Govern**: policies, accountability, culture.
- **Map**: understand the context, the intended use and the possible harms.
- **Measure**: test and track risks with metrics.
- **Manage**: prioritize, respond and monitor.

NIST also published a **Generative AI Profile** (NIST AI 600-1, July 2024) that applies the framework to generative AI risks such as confabulation, data privacy and information security.

## Example

Mapping one risk across all three, for a RAG customer-support bot:

| Framework | Entry |
|---|---|
| OWASP | LLM01:2026 Prompt injection (indirect, via retrieved documents) |
| MITRE ATLAS | The LLM prompt injection technique, used to reach exfiltration |
| NIST AI RMF | *Map*: identify retrieved documents as untrusted input. *Measure*: run injection tests every release. *Manage*: least-privilege tools and an incident playbook |

That one table is a credible start to a [threat model](../08-ai-system-design/threat-modeling.md).

## Common mistakes

- **Treating frameworks as the work.** Mapping IDs doesn't make a system safe. The controls do.
- **Using only one lens.** OWASP is good for builders, ATLAS for attacker paths, NIST for organizational process.
- **Citing old versions.** Check the edition date, as with the 2025 and 2026 OWASP lists.

## Check yourself

1. Which framework would you use to plan a red-team exercise, and why?
2. What are the four functions of the NIST AI RMF?
3. What is NIST AI 600-1?

<details>
<summary>Answers</summary>

1. MITRE ATLAS, because it catalogs attacker tactics and techniques step by step, with IDs, based on real attacks.
2. Govern, Map, Measure, Manage.
3. NIST's Generative AI Profile (2024), which applies the AI RMF to risks specific to generative AI.

</details>

## Go deeper

- [MITRE ATLAS](https://atlas.mitre.org/) - Browse the matrix and case studies. *Beginner · Website · 30 min*
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Overview and the full framework. *Intermediate · Standard · 1 h*
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) - The generative AI risk list. *Intermediate · PDF · 1 h*
