---
title: "LLM02: Sensitive information disclosure"
level: beginner
last_reviewed: 2026-11-14
---

# LLM02: Sensitive information disclosure

*OWASP LLM02:2026 · same ID in 2025*

## In one sentence

**Sensitive information disclosure** is when an LLM system exposes data that someone didn't authorize (personal details, credentials, business secrets, another customer's records) through its answers, tool calls, logs, or anywhere else its data flows.

## Why it matters in 2027

It's the one risk where OWASP says practitioner opinion and real incident data agree most strongly. Leaks also carry legal weight: under India's [DPDP Act](../08-ai-system-design/compliance-basics.md) and the EU's GDPR, exposing personal data can mean regulator complaints and penalties. And the leak paths have multiplied: answers, retrieved chunks, tool arguments, traces, prompts sent to third-party APIs.

## Explain it like I'm new

A helpful receptionist with access to every file in the building. Ask nicely, and they'll tell you anything they can see. They aren't malicious, just eager to help, and they don't really know who's allowed to see what. The fix isn't to train the receptionist to be suspicious. It's to only give them the files the current visitor is allowed to see.

## How it works

Data leaks out through four main routes:

| Route | Example |
|---|---|
| **What you send to the model** | Staff paste customer data or source code into a public chatbot, and the provider stores it |
| **What the model learned** | A model fine-tuned on support tickets repeats a customer's phone number word for word |
| **What the app retrieves** | RAG search returns another tenant's document because the index has no access filter |
| **Where outputs go** | Prompts and responses (with personal data) land in logs, traces or analytics tools that many people can read |

Research has shown that models can reproduce memorized training data verbatim when prompted the right way ([Carlini et al., 2021](https://arxiv.org/abs/2012.07805)).

**Defenses:**

- **Don't give the model data it doesn't need.** This is the strongest control. Filter retrieval by the current user's permissions *before* anything reaches the prompt.
- **Minimize and redact.** Remove or mask personal data (names, phone numbers, Aadhaar, card numbers) before sending prompts to a model or writing logs. See [PII and privacy](../03-ai-safety-guardrails/pii-and-privacy.md).
- **Scan outputs.** Check responses for secrets and personal data before showing or storing them.
- **Choose providers and settings deliberately.** Know whether your provider stores or trains on your data, and use business or zero-retention terms for sensitive work. Many free tiers allow the provider to use your data to improve its products.
- **Treat logs as sensitive.** Apply the same access rules and retention limits to traces as to the source data.
- **Be careful with fine-tuning on raw personal data.** Clean it first.

## Example

**A real case.** In 2023, Samsung engineers pasted confidential source code and meeting notes into ChatGPT to get help, which meant sending company data to an outside service. Samsung then restricted employee use of generative AI tools ([TechCrunch](https://techcrunch.com/2023/05/02/samsung-bans-use-of-generative-ai-tools-like-chatgpt-after-april-internal-data-leak/)). Nothing was hacked. The leak came from normal use without a policy or an approved tool.

**A common app bug.** An HR assistant answers "what's my leave balance?" by retrieving from an index of all employee records. A user asks "what's Priya's salary?" Retrieval happily returns her record, and the model answers. The prompt said "only discuss the user's own data", but the data was already in the context. The fix is a retrieval filter on `employee_id = current_user`.

## Common mistakes

- **Relying on instructions to keep secrets.** If data reaches the context, assume it can come out.
- **Logging full prompts and responses forever.** Logs are often the largest store of personal data in an AI app.
- **One shared index for all customers** with no per-tenant filtering.
- **Ignoring tool arguments.** An agent can leak data by putting it in a URL or an API call, not just in its answer.

## Check yourself

1. Name the four routes by which sensitive data leaks from an LLM system.
2. Why is a retrieval filter stronger than an instruction like "never reveal other users' data"?
3. Where, besides the model's answer, should you scan for personal data?

<details>
<summary>Answers</summary>

1. What you send to the model, what the model memorized in training, what the app retrieves, and where outputs and logs go.
2. The filter stops the data from ever reaching the model. An instruction can be ignored or overridden once the data is in the context.
3. Logs and traces, tool-call arguments, retrieved chunks, and any data sent to third-party services.

</details>

## Go deeper

- [OWASP LLM02: Sensitive information disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) - Official entry. *Beginner · Standard · 15 min*
- [Extracting Training Data from Large Language Models](https://arxiv.org/abs/2012.07805) - The research showing memorized data can be recovered. *Intermediate · Paper · 30 min*
- [Gemini API terms: how free and paid tiers use your data](https://ai.google.dev/gemini-api/terms) by Google - An example of why provider terms matter. *Beginner · Legal · 10 min*
