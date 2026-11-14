---
title: AI engineering roles in 2027
level: beginner
last_reviewed: 2026-11-14
---

# AI engineering roles in 2027

## In one sentence

The main AI engineering roles (AI engineer, AI safety or security engineer, forward-deployed AI engineer, and AI platform engineer) share one core of skills from this playbook and differ in where they spend most of their time: building features, breaking and defending systems, working with customers, or running shared infrastructure.

## Why it matters in 2027

Job titles in AI are inconsistent: the same title means different work at different companies, and new titles appear every year. Knowing what each role actually does helps you read job descriptions, choose what to learn next, and explain your fit in interviews. Across all of them, employers increasingly expect safety, security and production skills, not just the ability to call a model.

## Explain it like I'm new

A hospital. Doctors, surgeons, nurses and lab technicians all learned the same basics of biology and medicine, then specialized. A patient's care depends on all of them. AI teams are similar: everyone needs the foundations, and each role goes deeper in one direction.

## How it works

| Role | What you mostly do | Go deepest in | Typical evidence employers look for |
|---|---|---|---|
| **AI engineer** | Build AI features and agents into products: RAG, tools, prompts, evals | Modules [00](../00-foundations/README.md) to [02](../02-building-agents/README.md), [05](../05-evaluation/README.md), [07](../07-agent-ops-production/README.md) | Shipped projects with evals and clear READMEs |
| **AI safety / security engineer** | Threat-model AI systems, build guardrails, red-team, respond to incidents, work with compliance | Modules [03](../03-ai-safety-guardrails/README.md), [04](../04-llm-security/README.md), [05](../05-evaluation/README.md), [08](../08-ai-system-design/README.md) | Threat models, red-team write-ups, guardrail projects with measured false-positive rates |
| **Forward-deployed AI engineer** (FDE) | Work inside a customer's environment to make an AI product succeed: integrate data and systems, adapt workflows, handle security reviews | All modules, plus communication | End-to-end projects on messy real data; design docs; stories of working with non-technical stakeholders |
| **AI platform engineer** | Run shared infrastructure: gateways, model hosting, tracing, eval pipelines, cost controls | Modules [03](../03-ai-safety-guardrails/llm-gateways.md), [07](../07-agent-ops-production/README.md), [08](../08-ai-system-design/README.md) | Infrastructure projects, load tests, reliability work |

**The shared core** for all four: Python and software engineering basics, working fluently with [coding agents](../01-coding-agents/README.md), building and evaluating LLM apps, and the security and safety fundamentals. Someone who can build an agent but can't explain how it could be attacked, or how they'd measure it, is now a weak candidate for any of these roles.

**Where people come from:**

- **Software engineers**: strongest path into AI engineer, platform and FDE roles. Focus on evals, security and agent design.
- **Security engineers**: natural path into AI security. Focus on how LLMs work, prompt injection, agents and evals.
- **Data scientists and ML engineers**: strong on models and evaluation. Focus on production engineering, agents and security.
- **Students and career changers**: start with foundations and coding agents, then build the five projects.

## Example

Reading a job description. Suppose a posting asks for "experience securing LLM applications, familiarity with OWASP LLM Top 10, building evaluation pipelines, and working with customers on deployments." That's a blend of AI security and forward-deployed work. Evidence you could show from this playbook: [P2](../projects/p2-secure-rag/README.md) (attacks and defenses mapped to OWASP), [P4](../projects/p4-guardrailed-support-agent/README.md) (guardrails plus evals in CI), and the [P5](../projects/p5-production-capstone/README.md) threat model and design doc.

## Common mistakes

- **Chasing titles.** Read the responsibilities; titles vary widely.
- **Only building demos.** Employers look for evals, tests, threat models and production thinking.
- **Skipping security because "it's not my job".** In AI systems it's everyone's job.
- **Hiding how you used AI tools.** Be ready to explain your agent workflow and how you checked its output.

## Check yourself

1. What do all four roles have in common?
2. Which role spends most time inside customers' environments?
3. What project evidence fits an AI security role?

<details>
<summary>Answers</summary>

1. A shared core: software engineering, coding-agent fluency, building and evaluating LLM apps, and security and safety fundamentals.
2. The forward-deployed AI engineer.
3. Threat models, red-team write-ups, and guardrail projects with measured false-positive and false-negative rates, such as P2, P4 and the P5 threat model.

</details>

## Go deeper

- [OWASP GenAI Security Project](https://genai.owasp.org/) - The community most AI security practitioners take part in. *Beginner · Website · browse*
- [Building A Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html) by Chip Huyen - What platform engineers build. *Intermediate · Article · 40 min*
- [Your AI product needs evals](https://hamel.dev/blog/posts/evals/) by Hamel Husain - The eval mindset every role is expected to have. *Beginner · Article · 25 min*
