---
title: Memory and privacy
level: beginner
last_reviewed: 2026-11-14
---

# Memory and privacy

## In one sentence

An agent's long-term memory is a store of **personal data**, so it needs the same protections as any user database: collect only what's needed, tell users what's kept, keep it separate per user, protect it, and delete it when asked or when it's no longer needed.

## Why it matters in 2027

Memory turns casual chat into a growing profile of each user: health worries, money problems, family details. Privacy laws treat that as personal data. Under India's DPDP Act, whose main obligations apply from May 2027, and the EU's GDPR, people have rights to know what's held about them and to have it erased ([compliance basics](../08-ai-system-design/compliance-basics.md)). Users also lose trust fast when an assistant "remembers" something they didn't expect it to.

## Explain it like I'm new

A good family doctor remembers your history, and that's helpful. But you'd be upset if the receptionist could read it, if the doctor mentioned it in front of your boss, or if the file stayed in a cupboard forever after you moved away. Memory is helpful when it's expected, private and under your control.

## How it works

| Principle | What it means for agent memory |
|---|---|
| **Purpose** | Decide what memory is *for* ("personalize language and format", "remember project context"), and only save what serves that |
| **Minimization** | Prefer "prefers short answers" over storing the whole chat. Don't save sensitive categories (health, finances, religion) unless the feature truly needs it and the user agreed |
| **Transparency** | Tell users memory exists, show them what's remembered, and show when a memory is used |
| **Control** | Let users turn memory off, edit memories and delete them, individually or all at once |
| **Isolation** | Namespace every memory by user and tenant. Retrieval can never cross that boundary |
| **Retention** | Expire memories automatically after a set time unless renewed |
| **Complete deletion** | "Delete" must remove the memory from the store, its embeddings, caches, backups (on their schedule), and any eval datasets copied from it |
| **Security** | Encrypt at rest, restrict access, and log who reads memories |

> [!WARNING]
> Logs and traces often hold more personal data than the memory store itself, because they record every prompt. Apply the same retention and access rules to them ([observability](../07-agent-ops-production/observability-and-tracing.md)).

## Example

A memory settings design for a personal finance assistant:

```text
What I remember about you                                     [Turn memory off]

• Prefers answers in Hinglish                (you told me, 2 Nov 2026)   [Delete]
• Salary is credited on the 1st              (from your statements, 12 Oct)   [Delete]
• Saving for a car, target ₹6 lakh by 2027   (you told me, 3 Sep)   [Delete]

Memories older than 12 months are deleted automatically.          [Delete everything]
```

Behind it: each memory row stores `user_id`, `fact`, `source`, `created_at`, `expires_at`, and a link to its embedding so deletion removes both. The assistant never saves account numbers, card numbers or OTPs, which are filtered out before any write (see [PII and privacy](../03-ai-safety-guardrails/pii-and-privacy.md)).

## Common mistakes

- **Memory on by default with no notice.**
- **Deleting the row but not the embedding** (or the cache, or the copy in a trace).
- **Remembering sensitive details incidentally**, such as a health condition mentioned once in passing.
- **Using memories to train or tune models** without clear consent.

## Check yourself

1. Name four user controls a memory feature should offer.
2. Where else must data be removed when a user deletes a memory?
3. Why is "prefers short answers" better to store than the conversation it came from?

<details>
<summary>Answers</summary>

1. Any four of: knowing memory exists, seeing what's remembered, editing, deleting individual memories, deleting everything, turning memory off.
2. Its embeddings, caches, logs and traces, eval datasets, and backups on their normal schedule.
3. It serves the purpose with far less personal data, which is data minimization.

</details>

## Go deeper

- [Data protection framework](https://www.meity.gov.in/data-protection-framework) by MeitY - India's DPDP Act and Rules. *Beginner · Official page · 15 min*
- [Mem0 documentation](https://docs.mem0.ai) - An open-source memory layer; look at how it scopes and deletes memories. *Intermediate · Docs · 20 min*
- [OWASP LLM02: Sensitive information disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) - The security side of personal data in LLM apps. *Beginner · Standard · 15 min*
