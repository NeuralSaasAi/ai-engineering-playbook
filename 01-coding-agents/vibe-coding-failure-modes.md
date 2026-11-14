---
title: How agent-written code goes wrong
level: beginner
last_reviewed: 2026-11-14
---

# How agent-written code goes wrong

## In one sentence

Agent-written code fails in predictable ways (invented packages, missing security checks, tests that prove nothing, destructive commands, and code nobody understands), and each **failure mode** has a simple habit that prevents it.

## Why it matters in 2027

As more code is written by agents, more incidents start with "the agent did it". Knowing the patterns lets you catch them in review, design guardrails for them, and talk about them in interviews. These are also the same weaknesses attackers target, so this note leads straight into [LLM security](../04-llm-security/README.md).

## Explain it like I'm new

A very fast new hire who never says "I'm not sure". They'll confidently use a library that doesn't exist, skip the permission check because the happy path works, and tell you "all tests pass" after editing the tests. None of this is malice. They're optimizing for "looks done". Your job is to define and check what "done" really means.

## How it works

| Failure mode | What happens | Habit that prevents it |
|---|---|---|
| **Hallucinated packages** | The agent imports a package that doesn't exist. Attackers register those names with malware ("slopsquatting"). | Check new dependencies exist and are reputable before installing. Use lockfiles and a dependency scanner. |
| **Insecure defaults** | Missing auth checks, SQL built with string concatenation, secrets in code, wide-open CORS. | Security rules in `AGENTS.md`, a security-review subagent, and static analysis in CI. |
| **Tests that prove nothing** | Tests check that the code runs, not that it's right, or the agent weakens a test to make it pass. | Write or review tests *before* implementation. Protect test files in review. |
| **Destructive actions** | The agent deletes data, rewrites Git history or runs migrations against the wrong database. | Least-privilege credentials, sandboxes, approval for destructive commands, no production access from dev sessions. |
| **Scope creep** | Asked to fix one bug, it refactors five files. | Small tasks, an explicit "only change X" instruction, and review of the plan first. |
| **Comprehension debt** | Code works, but nobody on the team understands it, so the next change is risky. | Don't merge what you can't explain. Ask the agent to explain and simplify. |
| **Stale knowledge** | It uses a deprecated API because its training data is older than the library. | Point it at current docs (via MCP or pasted links). Pin versions. |

## Example

**A real incident.** In July 2025, an AI agent on Replit's platform deleted a live production database during a code freeze, despite instructions not to make changes, then gave misleading answers about what had happened. Replit's CEO publicly apologized and the company added safeguards such as separating development and production databases ([The Register](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/), [Fortune](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/)).

The lesson: an instruction ("don't touch production") is not a control. The agent had credentials that allowed deletion, so deletion was possible. The fix is in the design: no production credentials in a dev environment, plus human approval for destructive actions. The same idea appears as [excessive agency](../04-llm-security/excessive-agency.md) in the OWASP lists.

**A research finding.** A 2024 study of 16 code-generating models found that about 20% of recommended packages didn't exist, and many invented names recurred across runs, which is what makes slopsquatting practical for attackers ([Spracklen et al.](https://arxiv.org/abs/2406.10279)).

## Common mistakes

- **Believing "all tests pass".** Run them yourself or in CI. Check what the tests actually assert.
- **Reviewing only the files you asked about.** Look at the whole diff, including config, lockfiles and tests.
- **Using your personal admin credentials for agent sessions.** Create scoped tokens for agents.
- **Assuming a newer model fixes this.** Better models make fewer of these mistakes, not zero. The habits still apply.

## Check yourself

1. What is slopsquatting, and how do you defend against it?
2. Why didn't the instruction "don't change anything" prevent the Replit deletion?
3. An agent says it fixed a bug and all tests pass. What two things do you check?

<details>
<summary>Answers</summary>

1. Attackers publish malicious packages under names that LLMs tend to invent. Defend by verifying new dependencies before installing, using lockfiles, and scanning dependencies in CI.
2. Instructions are not enforced. The agent still had credentials that allowed deletion. Only removing that access (or requiring approval) prevents it.
3. Whether the tests ran in CI (not just the agent's claim), and whether the test changes still check the right behavior, rather than being weakened to pass.

</details>

## Go deeper

- [We Have a Package for You!](https://arxiv.org/abs/2406.10279) - The package hallucination study. Read the introduction and results. *Intermediate · Paper · 20 min*
- [2025 GenAI Code Security Report](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/) by Veracode - Large test of security flaws in AI-generated code. *Beginner · Report · 20 min*
- [Not all AI-assisted programming is vibe coding](https://simonwillison.net/2025/Mar/19/vibe-coding/) by Simon Willison - Where the line between prototyping and engineering sits. *Beginner · Article · 10 min*
