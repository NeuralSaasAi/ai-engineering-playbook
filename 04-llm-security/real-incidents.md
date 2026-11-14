---
title: Real incidents and what they teach
level: beginner
last_reviewed: 2026-11-14
---

# Real incidents and what they teach

## In one sentence

These verified incidents show the risks in this module happening to real companies, each with a source, what failed, and the design change that would have limited the damage.

## Why it matters in 2027

Interviewers, managers and auditors respond to real cases, not hypotheticals. Knowing a few incidents well, with accurate details, makes your security arguments credible. Repeating a dramatic but unverified story does the opposite, so every case here links to a primary source or reputable reporting.

## Explain it like I'm new

Aviation got safe by studying every crash and near-miss and changing designs and checklists so the same failure couldn't happen twice. AI engineering is early in that process. These are some of its first case files.

## How it works

For each incident, ask three questions: what was the entry point, what let the damage spread, and which control would have stopped it most cheaply. The answer to the third is almost always a design control (permissions, separation, approval) rather than a better prompt.

| Year | Incident | Risk | Key lesson |
|---|---|---|---|
| 2023 | Samsung staff paste confidential code into ChatGPT ([TechCrunch](https://techcrunch.com/2023/05/02/samsung-bans-use-of-generative-ai-tools-like-chatgpt-after-april-internal-data-leak/)) | [LLM02](sensitive-information-disclosure.md) | Approved tools and clear data rules prevent most leaks |
| 2023 | A car dealer's chatbot is talked into "agreeing" to sell a car for $1 ([Business Insider](https://www.businessinsider.com/car-dealership-chevrolet-chatbot-chatgpt-pranks-chevy-2023-12)) | [LLM01](prompt-injection.md) | Never let a chatbot make commitments; restrict its scope |
| 2024 | Air Canada held responsible for its chatbot's wrong refund advice ([The Guardian](https://www.theguardian.com/world/2024/feb/16/air-canada-chatbot-lawsuit)) | [LLM07](misinformation.md) | Policy answers must come from authoritative sources, and you own what your bot says |
| 2024 | Slack AI data exfiltration via planted message and rendered link ([PromptArmor](https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via)) | [LLM01](prompt-injection.md), [LLM10](improper-output-handling.md) | Untrusted content plus private data plus a way out is the lethal combination |
| 2025 | Malicious models on Hugging Face evade pickle scanning ([ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)) | [LLM04](supply-chain.md) | Load safe formats only; scan and pin |
| 2025 | Bybit loses about $1.5 billion after a supplier's developer machine is compromised ([FBI](https://www.ic3.gov/PSA/2025/PSA250226), [NCC Group](https://www.nccgroup.com/research/in-depth-technical-analysis-of-the-bybit-hack/)) | Supply chain (not AI-specific) | One compromised machine with deploy access can change what everyone downstream trusts |
| 2025 | EchoLeak: zero-click injection in Microsoft 365 Copilot ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-32711)) | [ASI01](agentic-threats.md) | Content an assistant reads automatically is an attack surface |
| 2025 | Replit agent deletes a production database during a code freeze ([The Register](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/)) | [LLM03](excessive-agency.md) | Instructions aren't controls; separate dev and prod access |
| 2025 | Fake Postmark MCP server BCCs every email to an attacker ([Koi Security](https://www.koi.ai/blog/postmark-mcp-npm-malicious-backdoor-email-theft)) | [LLM04](supply-chain.md), ASI04 | Pin and review agent extensions like code |

## Example

**Bybit, February 2025, in more detail.** On 21 February 2025, attackers the FBI attributed to North Korea's "TraderTraitor" group (also known as Lazarus) stole about $1.5 billion in Ethereum from a Bybit cold wallet. Bybit's own systems weren't the entry point. Investigators found that a developer machine at Safe{Wallet}, the multisig wallet provider Bybit used, had been compromised. The attackers used that access to change Safe{Wallet}'s web interface so that Bybit's signers saw a normal-looking transaction while actually approving one that handed control of the wallet to the attackers ([BleepingComputer](https://www.bleepingcomputer.com/news/security/lazarus-hacked-bybit-via-breached-safe-wallet-developer-machine/)).

Why it belongs in an AI playbook: coding agents and autonomous agents increasingly run on developer machines with deploy credentials. An agent that is tricked, or a machine that is compromised, can alter what downstream systems and people trust. The controls are the same ones this module teaches: least privilege for anything that can deploy, separation between development and production, independent verification of what's being signed or approved, and supply-chain integrity.

> [!NOTE]
> You'll sometimes see other incidents quoted with dramatic figures but no source. If you can't find a primary source or reputable reporting, don't repeat it. Precision is part of credibility.

## Common mistakes

- **Retelling incidents from memory** with wrong numbers or companies. Link the source.
- **Blaming "the AI".** In every case above, a design decision made the damage possible.
- **Only studying AI incidents.** Classic supply-chain and access-control failures apply directly to agents.

## Check yourself

1. In the Bybit incident, whose machine was the entry point?
2. Which two risks combined in the Slack AI case?
3. What did the Air Canada and Replit cases have in common?

<details>
<summary>Answers</summary>

1. A developer machine at Safe{Wallet}, a supplier, not Bybit itself.
2. Prompt injection (a planted message) and improper output handling (rendering a link that carried private data out).
3. In both, the organization relied on the AI behaving well instead of on controls. Air Canada relied on the chatbot being accurate; Replit relied on an instruction not to change production.

</details>

## Go deeper

- [AI Incident Database](https://incidentdatabase.ai/) - Searchable public records of AI harms. *Beginner · Database · browse*
- [FBI statement on the Bybit theft](https://www.ic3.gov/PSA/2025/PSA250226) - The official attribution. *Beginner · Notice · 5 min*
- [In-depth technical analysis of the Bybit hack](https://www.nccgroup.com/research/in-depth-technical-analysis-of-the-bybit-hack/) by NCC Group - How the attack worked, step by step. *Intermediate · Article · 25 min*
