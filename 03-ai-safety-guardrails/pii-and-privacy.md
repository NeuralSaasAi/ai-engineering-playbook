---
title: PII and privacy
level: beginner
last_reviewed: 2026-11-14
---

# PII and privacy

## In one sentence

**PII** (personally identifiable information) is any data that identifies a person, such as names, phone numbers, emails, Aadhaar or PAN numbers, card numbers or addresses, and protecting it in AI apps means detecting it, minimizing it, masking it before it reaches models and logs, and controlling who can see it.

## Why it matters in 2027

AI apps are full of personal data: support chats, uploaded documents, CRM records, voice transcripts. That data flows to model providers, vector stores, traces and evaluation datasets. India's DPDP Act's main obligations take effect in May 2027, and the EU's GDPR already applies, so careless handling has legal consequences ([compliance basics](../08-ai-system-design/compliance-basics.md)). Users also simply don't want their card number shown to a chatbot.

## Explain it like I'm new

A hospital receptionist who needs to book you an appointment doesn't need your full medical history. They see your name and the department. The doctor sees the rest. Each person sees only what their job needs, and the files are locked when they're not in use. Data minimization is the same idea for software.

## How it works

Four controls, in order of strength:

1. **Don't collect it.** If the feature doesn't need a date of birth, don't ask for it.
2. **Don't send it.** Remove or mask PII before text goes to the model, the vector store or the logs.
3. **Restrict access.** Retrieval only returns the current user's data ([sensitive information disclosure](../04-llm-security/sensitive-information-disclosure.md)).
4. **Delete on schedule.** Set retention limits for chats, logs and traces, and honor deletion requests everywhere, including embeddings.

**Detecting PII:**

| Method | Good at | Weak at |
|---|---|---|
| **Patterns (regex + checksums)** | Structured IDs: card numbers (with a Luhn checksum), emails, phone numbers, Aadhaar, PAN, IFSC | Names, addresses, free-text context |
| **Named-entity models** | Names, places, organizations | Speed; unusual names; mixed languages |
| **Tools that combine both** | Most real needs. [Microsoft Presidio](https://microsoft.github.io/presidio/) is a widely used open-source option with custom recognizers | Needs tuning for Indian formats and languages |

**Masking styles:**

- **Redact**: replace with a label. `My card is [CARD]`.
- **Pseudonymize**: replace with a consistent token you can reverse later on your server. `Call <PHONE_1>`, then swap back in the final message if the user is allowed to see it.
- **Partially mask**: `XXXX-XXXX-XXXX-4471`, when the last digits are useful.

## Example

```python
# test: run
import re

def luhn_ok(number: str) -> bool:
    digits = [int(d) for d in number][::-1]
    total = sum(d if i % 2 == 0 else (d * 2 - 9 if d * 2 > 9 else d * 2) for i, d in enumerate(digits))
    return total % 10 == 0

PATTERNS = {
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"),
    "PHONE_IN": re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"),
    "PAN": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
}
CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")

def redact(text: str) -> str:
    text = CARD.sub(lambda m: "[CARD]" if luhn_ok(re.sub(r"\D", "", m.group())) else m.group(), text)
    for label, pattern in PATTERNS.items():
        text = pattern.sub(f"[{label}]", text)
    return text

print(redact("I'm Ravi, ravi@example.com, phone 9876543210. "
             "Card 4111 1111 1111 1111, PAN ABCDE1234F, order 1234567890123."))
# I'm Ravi, [EMAIL], phone [PHONE_IN]. Card [CARD], PAN [PAN], order 1234567890123.
```

The order number isn't masked because it fails the Luhn check. That's how checksums cut false positives. Project [P4](../projects/p4-guardrailed-support-agent/README.md) uses a fuller version.

## Common mistakes

- **Masking the prompt but logging the original.** Logs and traces are often the biggest leak.
- **Regex only for names.** Patterns can't find names reliably. Use an entity model, or avoid needing to.
- **Forgetting embeddings and eval sets.** Vectors can leak text ([LLM09](../04-llm-security/vector-and-embedding-weaknesses.md)), and test data copied from production often contains real customers.
- **Free-tier APIs for real customer data** without checking whether the provider may use it.

## Check yourself

1. List the four privacy controls in order of strength.
2. Why use a checksum when detecting card numbers?
3. What's the difference between redaction and pseudonymization?

<details>
<summary>Answers</summary>

1. Don't collect it, don't send it, restrict access, delete on schedule.
2. It filters out long numbers that aren't card numbers, such as order IDs, which cuts false positives.
3. Redaction replaces the value with a label permanently. Pseudonymization replaces it with a consistent token that your server can map back to the original when appropriate.

</details>

## Go deeper

- [Microsoft Presidio](https://microsoft.github.io/presidio/) - Open-source PII detection and anonymization, with custom recognizers. *Beginner · Docs · 20 min*
- [Data protection framework](https://www.meity.gov.in/data-protection-framework) by MeitY - The DPDP Act and Rules, from the Government of India. *Beginner · Official page · 15 min*
- [OWASP LLM02: Sensitive information disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) - The security view of the same problem. *Beginner · Standard · 15 min*
