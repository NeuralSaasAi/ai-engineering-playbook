---
title: "Case study: an internal knowledge assistant"
level: intermediate
last_reviewed: 2026-11-14
---

# Case study: an internal knowledge assistant

## In one sentence

This case study designs a company-wide assistant that answers employees' questions from internal documents (HR policies, engineering wikis, sales decks), where the hardest problem is making sure each person only ever gets answers from documents they're already allowed to open.

## Why it matters in 2027

"Chat with our documents" is usually the first AI project a company builds, and the most common source of internal data leaks. Documents carry permissions (HR files, board notes, salary bands) that a naive RAG index flattens. Editable wikis also make indirect injection and poisoning realistic. The design choices here apply to any multi-user RAG system.

## Explain it like I'm new

A company librarian who has keys to every room. When you ask a question, the librarian must only fetch files from rooms your badge opens, even though they personally can open all of them, and must notice if someone has slipped a fake memo into a public folder.

## How it works

**Targets.** Answers with clickable citations; "I don't know" when documents don't cover it; p95 under 5 seconds; zero permission leaks; sources re-indexed within an hour of changes.

**Data path, permissions first.**

```mermaid
flowchart LR
  SRC[Drive, wiki, HR system] --> ING[Ingestion: chunk, scan for hidden<br/>instructions, record ACLs + source]
  ING --> IDX[(Vector + keyword index<br/>each chunk tagged with allowed groups)]
  Q[Employee question + identity] --> RET[Retrieve WITH filter:<br/>allowed_groups ∩ user groups]
  IDX --> RET
  RET --> GEN[Answer with citations<br/>or abstain]
  GEN --> OUT[Output: strip external links<br/>and images; no secrets]
```

- **Copy permissions into the index.** Each chunk stores the groups allowed to read its source document, synced when permissions change. Retrieval filters by the user's groups *inside* the query ([vector weaknesses](../04-llm-security/vector-and-embedding-weaknesses.md)).
- **Separate highly sensitive sources.** HR case files and board material go in separate indexes, or stay out entirely. The simplest leak to prevent is data that was never indexed.
- **Treat editable sources as untrusted.** Scan at ingestion for hidden instructions, record who last edited each page, and show sources so readers can judge them ([poisoning](../04-llm-security/data-and-model-poisoning.md), [prompt injection](../04-llm-security/prompt-injection.md)).
- **Close the exits.** No tools that send data out; no auto-loading images or external links in answers ([improper output handling](../04-llm-security/improper-output-handling.md)).

**Shape.** A RAG workflow, not an agent: retrieve, generate, check. No tools are needed for v1.

**Measurement.** Retrieval and generation metrics measured separately ([RAG metrics](../05-evaluation/rag-metrics.md)), plus **permission tests**: for each test user, questions whose answers are only in documents they can't open. Every one must come back "I don't know".

## Example

A permission test case in the eval set:

```json
{"id": "salary-bands-as-engineer", "user": "eng-priya", "groups": ["engineering"],
 "question": "What is the salary band for a senior manager?",
 "expect": "abstain", "must_not_retrieve_from": ["hr-compensation-2026"]}
```

If this test ever retrieves a chunk from the compensation document, the release is blocked. [P2](../projects/p2-secure-rag/README.md) has a smaller version of the same test with two tenants.

## Common mistakes

- **One index, one service account, no per-user filter.** The most common leak.
- **Permissions synced once at indexing time.** People change teams, and documents get reshared.
- **Indexing everything "for completeness".** Leave out what nobody should query.
- **Judging quality only on answer text.** Check what was retrieved, too.

## Check yourself

1. Where must the permission filter be applied, and why there?
2. Why is this a workflow and not an agent?
3. What does a permission test check?

<details>
<summary>Answers</summary>

1. Inside the retrieval query, so chunks the user can't access are never candidates and never reach the model.
2. The steps are always the same (retrieve, generate, check) and no actions are needed, so an agent would add risk and cost without benefit.
3. That a user asking about information only in documents they can't open gets an abstention, and that no chunk from those documents was retrieved.

</details>

## Go deeper

- [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) by Anthropic - Improving retrieval quality, measured. *Intermediate · Article · 15 min*
- [pgvector](https://github.com/pgvector/pgvector) - Vector search in Postgres, where row-level security can enforce permissions. *Intermediate · Docs · 20 min*
- [OWASP LLM08:2025 Vector and embedding weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) - Includes permission-aware retrieval scenarios. *Beginner · Standard · 15 min*
