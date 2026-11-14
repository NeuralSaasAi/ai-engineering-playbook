# Progress tracker

Where the playbook stands. Updated as work lands. Last update: **2026-11-14**.

**Legend:** ✅ done · 🟡 in progress · ⬜ not started

## Phase 1: content

| # | Task | Status | Notes |
|---|---|---|---|
| 1 | Scaffold, licenses, CI, note checker | ✅ | `scripts/check_notes.py` with 16 unit tests; runnable-snippet tests |
| 2 | Note template, style guide | ✅ | Glossary file still to write (task 11) |
| 3 | [00 · Foundations](00-foundations/README.md) | ✅ | 6 notes |
| 4 | [01 · Coding agents](01-coding-agents/README.md) + [P1](projects/p1-agent-built-cli/README.md) | ✅ | 8 notes; P1: 20 tests |
| 5 | [02 · Building agents](02-building-agents/README.md) | ✅ | 6 notes, LangGraph snippets tested |
| 6 | [04 · LLM security](04-llm-security/README.md) + [P2](projects/p2-secure-rag/README.md) | ✅ | 14 notes (OWASP LLM 2026, agentic, incidents, frameworks); P2: 26 tests + 5 expected failures |
| 7 | [03 · AI safety and guardrails](03-ai-safety-guardrails/README.md) | ✅ | 5 notes + defense-layers map |
| 8 | [05 · Evaluation](05-evaluation/README.md), [06 · Memory](06-agent-memory/README.md) + [P3](projects/p3-langgraph-research-agent/README.md) | ✅ | 8 notes; P3: 11 tests, eval 6/6 |
| 9 | [P4 · Guardrailed support agent](projects/p4-guardrailed-support-agent/README.md) | ✅ | 33 tests, eval 12/12 |
| 10 | 07 · Agent ops, 08 · System design + P5 capstone | 🟡 | P5 code and 5 tests done; README, threat model, design doc, Docker run and both modules to write |
| 11 | 09 · Careers, glossary, README, START-HERE, ABOUT | ⬜ | |
| 12 | Full `make check` green, then your review of the private repo | ⬜ | CI currently fails on links to pages not yet written; resolves with tasks 10 and 11 |

## Waiting on you

| Item | Why | One-time command |
|---|---|---|
| CI workflow not pushed yet | Your GitHub CLI token lacks the `workflow` scope, so GitHub refused `.github/workflows/checks.yml` (it's kept locally) | `gh auth refresh -h github.com -s workflow` |
| Fewer permission prompts | Kiro doesn't let the agent write its own permission file | `mkdir -p ~/.kiro/settings && cp .local/kiro-permissions.yaml ~/.kiro/settings/permissions.yaml` |

## Phase 2: website and polish

| # | Task | Status |
|---|---|---|
| 13 | MkDocs Material site built from the same markdown | ⬜ |
| 14 | Visual polish (brand colors, logo, home page cards) | ⬜ |
| 15 | Make public and deploy GitHub Pages (needs your yes) | ⬜ |
| 16 | Move to a NeuralSaas AI domain (needs your yes and a DNS change) | ⬜ |

## Decisions log

| Date | Decision |
|---|---|
| 2026-11-14 | Repo name `ai-engineering-playbook`; notes + 5 full projects; no reference to source video or roadmap.sh |
| 2026-11-14 | Default live model: Gemini free tier via LiteLLM; tests use fake models, no API keys in CI |
| 2026-11-14 | Security notes follow the **OWASP LLM Top 10 2026** (published Aug 2026), with 2025 IDs shown alongside |
| 2026-11-14 | Domain: start on github.io, then `learn.neuralsaasai.com` or `neuralsaasai.com/playbook` |
