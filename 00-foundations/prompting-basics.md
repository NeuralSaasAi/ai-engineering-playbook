---
title: Prompting basics
level: beginner
last_reviewed: 2026-11-14
---

# Prompting basics

## In one sentence

A **prompt** is the text you send to an LLM, and prompting well means giving it a clear role, the right context, a specific task and the output format you need.

## Why it matters in 2027

Prompts are now code. They sit in your repo, drive agents, and decide whether a tool call is safe. A vague prompt causes flaky behavior that no amount of model upgrades will fix. Writing precise instructions for coding agents (in files like `AGENTS.md`) is the same skill.

## Explain it like I'm new

Imagine briefing a smart new intern who knows nothing about your company. "Write something about our product" gets you a random essay. "You're writing for first-time customers. Using the attached feature list, write a 100-word welcome email. Friendly tone, no jargon, end with a link to the setup guide" gets you something usable.

Where the analogy stops working: an intern asks questions when confused. A model usually guesses, confidently.

## How it works

Most chat APIs split a prompt into **messages** with roles:

| Role | Who writes it | What it's for |
|---|---|---|
| `system` | You, the developer | Standing rules: who the assistant is, what it must and must not do, output format |
| `user` | The person using your app | Their request |
| `assistant` | The model | Its previous replies, resent to keep the conversation going |
| `tool` | Your code | Results from a function the model asked you to run (see [tool calling](../02-building-agents/tool-calling.md)) |

A reliable prompt usually has five parts:

1. **Role and audience.** "You are a support assistant for a banking app. Users are not technical."
2. **Context.** The facts the model needs, pasted in or retrieved. Don't make it rely on memory.
3. **Task.** One clear instruction, with limits: length, scope, what to do if information is missing.
4. **Examples.** One to three examples of good input and output. This is called **few-shot prompting** and is often the fastest way to fix format problems.
5. **Output format.** Plain text, bullet list, or JSON that your code will parse. For JSON, use the provider's structured-output feature where it exists.

Two techniques help with harder tasks:

- **Ask for reasoning before the answer**, or use a reasoning model that does this internally. Multi-step problems go better when the model works through them.
- **Break big jobs into steps.** Three focused prompts in a row usually beat one giant prompt. This idea leads directly to [agents](../02-building-agents/the-agent-loop.md).

> [!WARNING]
> A system prompt is not a security boundary. Users can often get the model to reveal or ignore it. Never put secrets in it, and enforce permissions in code. See [hidden context exposure](../04-llm-security/hidden-context-exposure.md).

## Example

Weak:

```text
Summarize this support ticket.
```

Better:

```text
System: You triage support tickets for an online store.
Return JSON only: {"category": one of ["billing","shipping","product","other"],
"urgency": "low"|"medium"|"high", "summary": string under 25 words}.
If the ticket mentions a legal threat or a safety issue, urgency is "high".

User: <ticket>My order #4471 arrived broken and the charger sparked when I plugged it in.</ticket>
```

The second version fixes the categories, defines urgency rules, limits length and makes the output machine-readable. Wrapping user text in tags like `<ticket>` also helps the model separate data from instructions (it helps, but doesn't make injection impossible).

## Common mistakes

- **Being vague about format.** If code parses the output, specify the exact schema and validate it.
- **Stuffing every rule into one prompt.** Long, contradictory instructions get partially ignored. Keep rules short and test them.
- **Not testing prompts.** Changing one word can change behavior. Keep a small set of test inputs and rerun them after every edit (see [evaluation](../05-evaluation/why-evals.md)).
- **Trusting the system prompt for safety.** Enforce rules in code too.

## Check yourself

1. What is the difference between a system message and a user message?
2. What is few-shot prompting, and when is it most useful?
3. Why shouldn't you put an API key in a system prompt?

<details>
<summary>Answers</summary>

1. The system message holds the developer's standing rules for the whole conversation. The user message is the end user's request.
2. Including a few worked examples of input and output in the prompt. It's most useful for fixing format and style problems.
3. Users can often trick the model into repeating its system prompt, so anything in it should be treated as public.

</details>

## Go deeper

- [Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) by Anthropic - Practical techniques with before-and-after examples. *Beginner · Docs · 30 min*
- [Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering) by OpenAI - Message roles, formatting and structured output. *Beginner · Docs · 20 min*
- [Prompting Guide](https://www.promptingguide.ai/) by DAIR.AI - Free reference covering most named prompting techniques. *Beginner · Website · browse*
