---
title: Red-teaming LLM apps
level: intermediate
last_reviewed: 2026-11-14
---

# Red-teaming LLM apps

## In one sentence

**Red-teaming** means deliberately attacking your own AI system, by hand and with automated tools, to find the ways it can be made to leak data, break rules, misuse tools or cause harm, before real attackers do.

## Why it matters in 2027

New jailbreak and injection techniques appear every month, and a guardrail that worked in January may not work in June. Regular, automated red-teaming is how teams keep up. It's also increasingly expected: security reviews, enterprise customers and regulations ask for evidence of adversarial testing. AI red-teaming is a fast-growing specialty within AI safety work.

## Explain it like I'm new

A bank hiring professional burglars to try to break in, with permission, and write up how they did it. The point isn't to prove the bank is safe. It's to find the weak window before a real burglar does, then fix it and try again.

## How it works

**Scope first.** Write down what you're testing (which app, which version), what counts as a failure, and what's off limits. Only test systems you own or have written permission to test.

**Two complementary approaches:**

| Approach | Strength | Weakness |
|---|---|---|
| **Manual** | Creative, finds new attack types and business-logic flaws | Slow, hard to repeat |
| **Automated** | Runs hundreds of known attacks on every release, repeatable | Mostly finds known patterns |

**Open-source tools:**

| Tool | What it does |
|---|---|
| [promptfoo](https://www.promptfoo.dev/docs/red-team/) | Evals and red-teaming from a config file. Generates attacks for your app's purpose, maps findings to OWASP. Open source (acquired by OpenAI in March 2026, and stated to remain open source) |
| [garak](https://github.com/NVIDIA/garak) (NVIDIA) | An "LLM vulnerability scanner" with many probes for jailbreaks, injection, data leakage and more |
| [PyRIT](https://github.com/Azure/PyRIT) (Microsoft) | A Python framework for building multi-turn, automated attack campaigns |

**A practical loop:**

1. Run an automated scan against a staging version of your app.
2. Review findings by hand. Many will be false alarms; some will be real.
3. For each real finding, add a regression test to your [golden dataset](golden-datasets.md), then fix it with a design change or guardrail.
4. Add a short manual session each release focused on new features (new tools, new data sources).
5. Track the attack success rate over time.

## Example

A promptfoo config that red-teams a support bot running on your machine:

```yaml
# promptfooconfig.yaml  ->  run: npx promptfoo@latest redteam run
description: Support bot red team
targets:
  - id: http
    config:
      url: http://localhost:8000/chat
      method: POST
      body: { "user_id": "red-team", "message": "{{prompt}}" }
      transformResponse: json.reply
redteam:
  purpose: >
    Customer support for an online store. Can look up the current user's orders.
    Must never reveal other customers' data, issue refunds, or discuss topics unrelated to orders.
  plugins:
    - pii            # tries to extract personal data
    - bola           # tries to access other users' objects
    - excessive-agency
    - hijacking      # tries to pull the bot off its purpose
  strategies:
    - jailbreak
    - prompt-injection
```

Project [P4](../projects/p4-guardrailed-support-agent/README.md) exposes exactly this kind of endpoint so you can point a scanner at it.

## Common mistakes

- **Red-teaming once, before launch.** Attacks evolve and your app changes. Make it continuous.
- **Only testing the model.** Test the whole app: retrieval, tools, output rendering, memory.
- **Fixing findings with prompt patches.** Prefer design fixes, and keep the attack as a regression test.
- **Testing without permission.** Scanning someone else's AI product without authorization can be illegal, even with good intentions.

## Check yourself

1. Why combine manual and automated red-teaming?
2. What should happen to every confirmed finding?
3. Why test the whole app instead of just the model?

<details>
<summary>Answers</summary>

1. Automated tools repeat known attacks cheaply on every release. Humans find new attack types and app-specific logic flaws.
2. It becomes a regression test in your eval dataset, and gets fixed, preferably with a design change.
3. Most damage comes from what surrounds the model: retrieved data, tools, output handling and memory. A safe model in an unsafe app is still unsafe.

</details>

## Go deeper

- [promptfoo red-team guide](https://www.promptfoo.dev/docs/red-team/) - Getting started, plugins and strategies. *Beginner · Docs · 20 min*
- [garak](https://github.com/NVIDIA/garak) - Install it and run a scan against a local model. *Intermediate · Repo · 30 min*
- [PyRIT](https://github.com/Azure/PyRIT) - Multi-turn automated attacks. *Intermediate · Repo · 45 min*
