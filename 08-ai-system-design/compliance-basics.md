---
title: Compliance basics for AI engineers
level: beginner
last_reviewed: 2026-11-14
---

# Compliance basics for AI engineers

## In one sentence

**AI compliance** means building systems that meet the laws and standards that apply to them, mainly data-protection laws such as India's DPDP Act and the EU's GDPR, and AI-specific rules such as the EU AI Act, by designing in the right controls and keeping the records that prove it.

## Why it matters in 2027

Two big deadlines land in 2027. Most obligations under India's DPDP Rules apply from **May 2027**, eighteen months after the Rules were notified on 13 November 2025 ([IBA summary](https://www.ibanet.org/The-practicalities-of-implimenting-India-digital-personal-data-protection-act)). The EU AI Act's rules for high-risk systems listed in Annex III now apply from **2 December 2027**, after the AI Omnibus amendment delayed them ([European Commission](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force)). Engineers who understand what these require can design compliant systems from the start instead of retrofitting them.

> [!IMPORTANT]
> This note is an engineer's orientation, not legal advice. Work with your legal or compliance team on any real decision.

## Explain it like I'm new

Building codes for houses. Inspectors don't care which brand of bricks you used. They check that there are fire exits, the wiring is safe, and you have the paperwork. Compliance for AI is similar: regulators care that personal data is handled lawfully, risks are assessed, people are informed, and you can show your records.

## How it works

**India: Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025**

- Applies to digital personal data processed in India, and to processing abroad when it relates to offering goods or services to people in India.
- **Consent** must be free, specific, informed and unambiguous, with a clear notice. People can withdraw it as easily as they gave it.
- **Data principals** (the people the data is about) have rights to access, correct and erase their data, and to grievance redressal.
- **Data fiduciaries** (organizations deciding how data is used) must use reasonable security safeguards, report breaches, and delete data when its purpose is served.
- The Data Protection Board can impose penalties of up to ₹250 crore per instance for some failures, such as not taking reasonable security safeguards.
- Rollout: the Board from November 2025, consent-manager registration from November 2026, most remaining obligations from May 2027.

**EU: AI Act** (risk-based; applies to AI placed on the EU market or affecting people in the EU, wherever the provider is)

| Category | Examples | What applies |
|---|---|---|
| Prohibited | Social scoring, some manipulative or exploitative systems | Banned since February 2025 |
| High-risk (Annex III) | AI in hiring, credit scoring, education, access to essential services | Risk management, data governance, logging, human oversight, accuracy and security requirements; from 2 December 2027 |
| Transparency obligations | Chatbots, AI-generated content | Tell people they're dealing with AI; label synthetic content |
| General-purpose AI models | Large foundation models | Documentation and copyright obligations for providers, since August 2025 |

**GDPR** applies to EU personal data and overlaps heavily with DPDP: lawful basis, minimization, rights, security, breach notification.

**What this means for your designs:**

| Requirement | Engineering control |
|---|---|
| Purpose limitation, minimization | Collect only what's needed; mask PII before models and logs ([PII and privacy](../03-ai-safety-guardrails/pii-and-privacy.md)) |
| Right to erasure | Deletion that reaches stores, embeddings, caches and traces ([memory and privacy](../06-agent-memory/memory-privacy.md)) |
| Security safeguards | Access control, encryption, least privilege, the defenses in [module 04](../04-llm-security/README.md) |
| Transparency | Tell users when they're talking to AI; show sources |
| Human oversight | Approval steps for high-impact decisions ([human-in-the-loop](../02-building-agents/human-in-the-loop.md)) |
| Records and accountability | Traces, eval results, threat models, change history ([deployment](../07-agent-ops-production/deploying-agents.md)) |

## Example

A hiring startup screens CVs with an LLM for clients in India and the EU. Engineering implications: in the EU this is likely a high-risk use (employment), so plan for risk management, logging, human review of every rejection, bias evaluation on the eval set, and documentation. Under DPDP: a clear consent notice for candidates, purpose-limited retention (delete CVs after the hiring round unless the candidate opts in), PII masking in logs, and a way for candidates to access and erase their data.

## Common mistakes

- **Treating compliance as a launch-week task.** Deletion, logging and consent are hard to add later.
- **Sending personal data to free-tier APIs** whose terms allow the provider to use it.
- **"We don't store data"** while traces, caches and vector indexes do.
- **Assuming the law doesn't apply abroad.** Both DPDP and the EU AI Act reach outside their borders.

## Check yourself

1. When do most DPDP Rules obligations apply?
2. Name two uses the EU AI Act treats as high-risk.
3. Which engineering controls support the right to erasure?

<details>
<summary>Answers</summary>

1. From May 2027, eighteen months after the Rules were notified in November 2025.
2. Any two of: hiring and worker management, credit scoring, education, access to essential services (Annex III).
3. Deletion that covers primary stores, embeddings and vector indexes, caches, logs and traces, eval datasets, and backups on their schedule.

</details>

## Go deeper

- [Data protection framework](https://www.meity.gov.in/data-protection-framework) by MeitY - The DPDP Act and Rules from the Government of India. *Beginner · Official page · 15 min*
- [AI Act regulatory framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) by the European Commission - Official overview and timeline. *Beginner · Official page · 15 min*
- [EU AI Act explorer](https://artificialintelligenceact.eu/) - Searchable text of the Act with summaries. *Intermediate · Website · browse*
