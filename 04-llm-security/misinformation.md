---
title: "LLM07: Misinformation"
level: beginner
last_reviewed: 2026-11-14
---

# LLM07: Misinformation

*OWASP LLM07:2026 · was LLM09 in 2025*

## In one sentence

**Misinformation**, in OWASP's sense, is when an LLM produces wrong, incomplete or unsupported output that looks credible enough that a person, a workflow or an agent acts on it.

## Why it matters in 2027

OWASP's 2026 edition singles this one out. Practitioners voted it near the bottom, but the record of real incidents put it near the top, the widest gap in the direction that hurts. In agent systems, a wrong answer becomes a wrong action: a refund issued, a config changed, a patient told the wrong dose. Companies have also been held responsible for what their chatbots say.

## Explain it like I'm new

A very confident tour guide who never says "I don't know". When they know the answer, they're great. When they don't, they make up an answer in exactly the same confident voice. The danger isn't that they're sometimes wrong. It's that you can't tell which answers are the wrong ones.

## How it works

Causes:

- **Hallucination**: the model generates plausible but false content ([how LLMs work](../00-foundations/how-llms-work.md)).
- **Weak grounding**: the right source wasn't retrieved, or the model ignored it.
- **Stale or poisoned context**: the source itself is out of date or tampered with ([poisoning](data-and-model-poisoning.md)).
- **Overreliance**: people and downstream systems trust output without checking. In agents, one agent's wrong output becomes another's trusted input.

**Defenses:**

- **Ground answers in sources** with [RAG](../00-foundations/rag-in-one-page.md), and require citations users can click.
- **Allow "I don't know".** Tell the model to abstain when sources don't cover the question, and test that it does.
- **Verify before acting.** For high-impact outputs, check against a system of record in code. If the model says "the customer is eligible for a refund", the refund tool checks eligibility itself.
- **Measure** factual accuracy and faithfulness to sources with [evals](../05-evaluation/README.md).
- **Design the interface for doubt.** Show sources and confidence, label AI output, and make it easy to escalate to a human.
- **Restrict domains.** A support bot shouldn't answer legal or medical questions at all.

## Example

**A real case.** In 2024, a Canadian tribunal ordered Air Canada to compensate a customer after its website chatbot gave wrong information about bereavement fares. The airline argued the chatbot was responsible for its own statements. The tribunal rejected that and held the company responsible for information on its own website ([The Guardian](https://www.theguardian.com/world/2024/feb/16/air-canada-chatbot-lawsuit)).

The engineering lesson: answers about policies, prices and eligibility should come from the authoritative policy text (retrieved and cited) or from a system of record, with a clear path to a human, never from the model's general knowledge.

## Common mistakes

- **Using the model's built-in knowledge for facts that matter.** Retrieve them.
- **Treating citations as proof.** Models can cite a source that doesn't say what they claim. Check faithfulness in evals.
- **Letting agent outputs flow into actions unchecked.**
- **Measuring only "helpfulness".** Measure accuracy and abstention too.

## Check yourself

1. Why is misinformation a security risk and not just a quality problem?
2. What did the Air Canada tribunal decide about responsibility for chatbot answers?
3. An agent says "this user qualifies for a ₹10,000 credit". What should happen before the credit is issued?

<details>
<summary>Answers</summary>

1. Because wrong output gets acted on: it drives decisions, tool calls and other agents, causing financial, legal or safety harm.
2. That the company is responsible for information its chatbot gives on its website, just like any other page.
3. The credit tool, in code, checks eligibility against the system of record, and for that amount a human probably approves.

</details>

## Go deeper

- [OWASP LLM09:2025 Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/) - Official entry. *Beginner · Standard · 15 min*
- [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) - The project leads' letter explains the vote-versus-evidence gap. *Beginner · Standard · 10 min*
- [Air Canada chatbot case](https://www.theguardian.com/world/2024/feb/16/air-canada-chatbot-lawsuit) - Short news report. *Beginner · Article · 5 min*
