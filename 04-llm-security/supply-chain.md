---
title: "LLM04: Supply chain"
level: intermediate
last_reviewed: 2026-11-14
---

# LLM04: Supply chain

*OWASP LLM04:2026 · was LLM03 in 2025*

## In one sentence

An LLM **supply chain** attack compromises something your app depends on (a model file, a fine-tuning adapter, a dataset, a Python package, an MCP server, an agent skill) so that the attacker's code or behavior arrives inside your system through a trusted channel.

## Why it matters in 2027

AI apps pull in more third-party parts than most software: open models from hubs, adapters, datasets, framework plugins, MCP servers and skills, often installed with one command. Many of these can run code. Attackers know developers trust what they download, and agents now install things too.

## Explain it like I'm new

A restaurant can have a spotless kitchen and still poison customers if a supplier's spices were contaminated. You can't inspect every grain, so you buy from trusted suppliers, check seals, track batch numbers and know what to recall if something goes wrong.

## How it works

| Component | How it goes wrong |
|---|---|
| **Model files** | Older formats like Python pickle can run arbitrary code when loaded. A model can also be swapped for a look-alike with hidden behavior. |
| **Adapters (LoRA) and merges** | Small add-on weights from unknown authors can change model behavior in subtle ways. |
| **Datasets** | Public datasets can contain poisoned samples (see [poisoning](data-and-model-poisoning.md)). |
| **Packages** | Typosquatted or hallucinated package names carry malware ([slopsquatting](../01-coding-agents/vibe-coding-failure-modes.md)). |
| **MCP servers, plugins, skills** | Tool descriptions and skill files are text the model reads, and servers run code with your credentials ([MCP](../01-coding-agents/mcp.md), [skills](../01-coding-agents/skills.md)). |
| **Hosted APIs** | A provider changes a model behind the same name, or has an outage or breach. |

**Defenses:**

- **Prefer safe formats.** Load models as [safetensors](https://github.com/huggingface/safetensors), which stores weights only and can't run code. Avoid loading pickle files from unknown sources ([Hugging Face guidance](https://huggingface.co/docs/hub/security-pickle)).
- **Allowlist and pin.** Use known publishers, pin versions and checksums (hashes), and use lockfiles (`uv.lock`) so builds are reproducible.
- **Keep an inventory.** A software bill of materials (SBOM), and for AI an AI-BOM, lists every model, dataset and package you use, so you can respond when one is found to be bad.
- **Scan.** Dependency scanners in CI, and model scanners for pickle payloads.
- **Review third-party agent extensions** like you review code: read the skill or server, check who publishes it, limit its credentials.
- **Pin hosted model versions** and re-run your [evals](../05-evaluation/README.md) before upgrading.

## Example

**Malicious models.** In February 2025, ReversingLabs reported models on Hugging Face that used deliberately broken pickle files to slip past the hub's scanner and run code when loaded ([ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)).

**A malicious MCP server.** In September 2025, researchers found an npm package impersonating a legitimate Postmark email MCP server. After several clean releases, an update silently added the attacker's address as BCC on every email the agent sent ([Koi Security](https://www.koi.ai/blog/postmark-mcp-npm-malicious-backdoor-email-theft)). Pinning versions and reviewing updates would have contained it.

**Not AI-specific, same lesson.** The February 2025 Bybit theft of about $1.5 billion began with a compromised developer machine at Safe{Wallet}, a supplier, whose web interface was then altered to trick Bybit's signers ([NCC Group analysis](https://www.nccgroup.com/research/in-depth-technical-analysis-of-the-bybit-hack/)). See [real incidents](real-incidents.md).

## Common mistakes

- **`pip install` whatever the agent suggests** without checking the package exists and is the real one.
- **Auto-updating extensions.** A safe version today can be replaced by a malicious one tomorrow.
- **Loading `.bin` or `.pkl` models from strangers.**
- **No inventory,** so when a component is reported compromised, you can't tell if you use it.

## Check yourself

1. Why is loading a pickle-format model from an unknown source dangerous?
2. What does pinning protect against in the Postmark MCP case?
3. What is an AI-BOM for?

<details>
<summary>Answers</summary>

1. Pickle files can contain code that runs when the file is loaded, so loading the model can compromise your machine.
2. It stops a later malicious update from being installed automatically. You keep running the version you reviewed.
3. Listing every model, dataset, adapter and package your system uses, so you can find and respond to compromised components quickly.

</details>

## Go deeper

- [OWASP LLM03:2025 Supply chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/) - Official entry. *Beginner · Standard · 15 min*
- [Pickle scanning on Hugging Face](https://huggingface.co/docs/hub/security-pickle) - Why pickle is risky and what the hub checks. *Beginner · Docs · 10 min*
- [SLSA](https://slsa.dev) - A framework for supply-chain integrity levels. *Intermediate · Website · 20 min*
