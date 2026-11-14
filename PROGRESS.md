# Progress tracker

Where the playbook stands. Updated as work lands. Last update: **2026-11-14**.

**Legend:** ✅ done · 🟡 in progress · ⬜ not started

## Phase 1: content ✅

| # | Task | Status | Notes |
|---|---|---|---|
| 1 | Scaffold, licenses, CI, note checker | ✅ | `scripts/check_notes.py` (16 unit tests) and runnable-snippet tests (8 snippets) |
| 2 | Note template, style guide, glossary | ✅ | 70 glossary terms |
| 3 | [00 · Foundations](00-foundations/README.md) | ✅ | 6 notes |
| 4 | [01 · Coding agents](01-coding-agents/README.md) + [P1](projects/p1-agent-built-cli/README.md) | ✅ | 8 notes; P1: 20 tests |
| 5 | [02 · Building agents](02-building-agents/README.md) | ✅ | 6 notes |
| 6 | [04 · LLM security](04-llm-security/README.md) + [P2](projects/p2-secure-rag/README.md) | ✅ | 13 notes (OWASP LLM 2026, agentic, incidents, frameworks); P2: 26 tests + 5 expected failures |
| 7 | [03 · AI safety and guardrails](03-ai-safety-guardrails/README.md) | ✅ | 5 notes + defense-layers map |
| 8 | [05 · Evaluation](05-evaluation/README.md), [06 · Memory](06-agent-memory/README.md) + [P3](projects/p3-langgraph-research-agent/README.md) | ✅ | 8 notes; P3: 11 tests, eval 6/6 |
| 9 | [P4 · Guardrailed support agent](projects/p4-guardrailed-support-agent/README.md) | ✅ | 33 tests, eval 12/12 |
| 10 | [07 · Agent ops](07-agent-ops-production/README.md), [08 · System design](08-ai-system-design/README.md) + [P5](projects/p5-production-capstone/README.md) | ✅ | 10 notes incl. 3 case studies; P5: 5 tests, Docker + Jaeger verified, design doc, threat model |
| 11 | [09 · Careers](09-careers-2027/README.md), [glossary](glossary.md), [README](README.md), [START-HERE](START-HERE.md), [ABOUT](ABOUT.md) | ✅ | 4 career notes |
| 12 | All checks green; your review of the private repo | 🟡 | 60 notes pass the checker; 0 markdown lint issues; 304 unique links OK; all project tests pass in CI. **Waiting for your review** |

## Phase 2: website and polish

| # | Task | Status |
|---|---|---|
| 13 | MkDocs Material site built from the same markdown | ✅ |
| 14 | Visual polish (brand colors, logo, home page cards) | ✅ |
| 15 | Make public and deploy GitHub Pages (needs your yes) | 🟡 Deploy workflow ready; waiting for your yes to make the repo public |
| 16 | Move to a NeuralSaas AI domain (needs your yes and a DNS change) | ⬜ |

## Website details

- Built with MkDocs Material from the repo root (`mkdocs.yml`, `site_hooks.py`, `overrides/`, `assets/`). The notes are unchanged.
- Navigation is generated from each module README's table, so adding a note to a module README adds it to the site.
- Links to code and data files point to GitHub automatically.
- SEO: canonical URLs, `sitemap.xml`, `robots.txt`, Open Graph and Twitter cards with `assets/social-card.png`.
- The site URL comes from the `SITE_URL` repository variable, so the custom-domain move is a config change.
- Preview locally: `make site-serve`.
- Watch item: MkDocs 1.x is no longer actively maintained, and the Material team points to its successor (Zensical). The build is pinned and works today. Re-evaluate in 2027.

## Optional for you

| Item | Command |
|---|---|
| Upload the GitHub social preview (Settings > General > Social preview) | Use `assets/social-card.png` |
| Fewer permission prompts in Kiro | `mkdir -p ~/.kiro/settings && cp .local/kiro-permissions.yaml ~/.kiro/settings/permissions.yaml` |

## Known limits and follow-ups

- Projects use deliberately simple, regex-based guardrails and fake models so they run offline. Each README suggests swapping in real libraries and models as an exercise.
- P5's rate limiter keeps counters in memory, so the container runs one worker. Verified: with two workers each process counted separately and no requests were limited.
- Prices and plan names in [the tool comparison](01-coding-agents/tool-comparison.md) are as of 14 Nov 2026 and need a monthly re-check.

## Decisions log

| Date | Decision |
|---|---|
| 2026-11-14 | Repo name `ai-engineering-playbook`; notes + 5 full projects; no reference to source video or roadmap.sh |
| 2026-11-14 | Default live model: Gemini free tier via LiteLLM; tests use fake models, no API keys in CI |
| 2026-11-14 | Security notes follow the **OWASP LLM Top 10 2026** (published Aug 2026), with 2025 IDs shown alongside |
| 2026-11-14 | Domain: start on github.io, then `learn.neuralsaasai.com` or `neuralsaasai.com/playbook` |
