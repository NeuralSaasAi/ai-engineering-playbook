# Style guide

This playbook exists to help people understand things, not to collect links. Every rule below serves that goal.

## Who we write for

A reader who can write basic Python and has used ChatGPT or a similar assistant, but has never built an AI application. By the end of a module they should be able to explain each idea to a colleague and use it in a small project.

## How a note is built

Every concept note uses [templates/note-template.md](templates/note-template.md). The sections are fixed, in this order:

1. **In one sentence**: the idea in plain words.
2. **Why it matters in 2027**: what goes wrong, costs money, or gets asked in interviews if you don't know it.
3. **Explain it like I'm new**: an everyday analogy, plus where it stops working.
4. **How it works**: the real explanation, with a diagram where it helps.
5. **Example**: something concrete.
6. **Common mistakes**.
7. **Check yourself**: three questions, answers hidden in `<details>`.
8. **Go deeper**: two to four sources, each tagged with level, format and time.

`scripts/check_notes.py` enforces the structure, so CI fails if a section is missing.

## Writing rules

- **Short.** Aim for 500 to 800 words. If a note passes 800, split it into two notes rather than compress it.
- **Plain words.** Define every technical term the first time you use it, and add it to [glossary.md](glossary.md). Bold terms in the first section must have a glossary entry (CI checks this).
- **One idea per sentence.** Use active voice. Prefer periods and commas over long dash chains.
- **Real size.** Describe things at their actual size. No "revolutionary", "game-changing", "robust", "leverage", "delve" or "landscape".
- **Specific.** Name the mechanism, the number and the source. "Llama Guard classifies prompts against a list of hazard categories" beats "Llama Guard keeps you safe".
- **Original.** Write in your own words. Never copy text from courses, books, videos or other sites. Short quotes (under 30 words) are fine when they are clearly marked and cited.
- **No promotion.** No course, product or affiliate links inside notes. Tools are named because readers will meet them at work, not because anyone asked.

## Sources

Good sources, in order of preference:

1. Official documentation and standards (OWASP, NIST, MITRE, vendor docs, regulation text).
2. Original research papers and engineering blogs from the team that built the thing.
3. Reputable reporting with named sources, for incidents.

Every factual claim that might change (prices, rankings, dates, versions, incident figures) needs a link. Date-sensitive facts carry "as of" wording, and every note has a `last_reviewed` date in its front matter.

When a popular claim can't be verified, leave it out. Don't repeat it with a disclaimer.

## Formatting: one source for GitHub and the website

The same markdown files are read on github.com and built into the website. Only use features that render correctly in both places:

| Need | Use | Don't use |
|---|---|---|
| Side notes, warnings | GitHub alerts: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]` | `!!! note` (MkDocs) or `{: .note}` (Jekyll) |
| Diagrams | Code fences marked `mermaid` | Screenshots of diagrams |
| Hidden answers | `<details><summary>Answers</summary> ... </details>`, with a blank line after `<summary>` | Custom widgets |
| Links between pages | Relative paths to `.md` files, e.g. `../04-llm-security/prompt-injection.md` | Absolute website URLs |
| Everything else | Standard GitHub-flavored markdown: tables, code fences, task lists | Shortcodes, Liquid tags, HTML layouts |

Front matter is three fields only:

```yaml
---
title: What is an embedding?
level: beginner          # beginner | intermediate
last_reviewed: 2026-11-14
---
```

Each folder has a `README.md` that works as its index page, both on GitHub and on the site.

## Code in notes

- Keep snippets short (under ~30 lines) and runnable.
- Python 3.12. Use the same libraries as the projects (LiteLLM, LangGraph).
- Never put a real API key in an example. Read keys from environment variables.
