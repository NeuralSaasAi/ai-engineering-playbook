---
title: "LLM09: Vector and embedding weaknesses"
level: intermediate
last_reviewed: 2026-11-14
---

# LLM09: Vector and embedding weaknesses

*OWASP LLM09:2026 · was LLM08 in 2025*

## In one sentence

**Vector and embedding weaknesses** are security problems in the similarity-search layer of an AI app (RAG indexes, vector-backed memory, semantic caches) where retrieval returns the wrong data, leaks data across users, or can be manipulated, even when no instruction is injected at all.

## Why it matters in 2027

Almost every LLM product that uses private data has a vector index between the data and the prompt. That makes the index part of your trust boundary. OWASP's 2026 entry sums the risks up neatly: poisoning makes the system wrong, inversion makes it leak, and jamming makes it fail to find the right answer.

## Explain it like I'm new

A shared filing room where every department's documents are stored together, and a fast clerk fetches "the most similar files" for any request. If the clerk doesn't check badges, anyone gets anyone's files. If someone sneaks in files that look very similar to common requests, those get fetched first. And the folder labels themselves can say a lot about what's inside.

## How it works

| Weakness | What goes wrong | Defense |
|---|---|---|
| **Missing access control** | One index holds many users' or tenants' data, and search doesn't filter by permission | Filter every query by tenant and user permissions, at the database level. Consider separate indexes per tenant. |
| **Retrieval poisoning** | Crafted documents are written to be "closest" to common questions, so they win retrieval ([PoisonedRAG](https://arxiv.org/abs/2402.07867)) | Control who can add documents, track provenance, review new sources |
| **Embedding inversion** | Text can be partly reconstructed from its embedding vector ([Morris et al., 2023](https://arxiv.org/abs/2310.06816)) | Treat vectors as being as sensitive as the source text. Encrypt, restrict access, don't share them casually |
| **Retrieval jamming** | Junk or near-duplicate content crowds out the right chunks | Deduplicate, cap results per source, use hybrid search and reranking |
| **Semantic cache leaks** | A cache returns a stored answer for "similar" questions, including another user's personalized answer | Scope caches per user or only cache non-personal answers |
| **Stale data** | Deleted or changed documents remain in the index | Sync deletions; re-index on change; honor data-deletion requests |

## Example

A B2B SaaS app adds "Ask your docs". All customers' documents go into one vector collection with a `tenant_id` field in metadata. The first version filters results *after* retrieval, in Python:

```python
hits = index.search(query_vector, top_k=5)
hits = [h for h in hits if h.metadata["tenant_id"] == user.tenant_id]
```

Two problems. If the top 5 are all from another tenant, the user gets nothing useful. And one forgotten filter in a new code path leaks other customers' data. The safer version filters *inside* the query, so other tenants' vectors are never candidates:

```python
hits = index.search(query_vector, top_k=5, filter={"tenant_id": user.tenant_id})
```

Even better for strict isolation: a separate collection or database schema per tenant. Project [P2](../projects/p2-secure-rag/README.md) tests exactly this.

## Common mistakes

- **Thinking vectors are anonymous.** They can leak the text they came from.
- **Filtering after retrieval** instead of inside the query.
- **Forgetting deletions.** "Delete my data" must remove vectors too.
- **Letting users upload into a shared index** that others search.

## Check yourself

1. What's the difference between retrieval poisoning and prompt injection?
2. Why is filtering inside the vector query safer than filtering the results afterwards?
3. Why should embeddings be protected like the original text?

<details>
<summary>Answers</summary>

1. Retrieval poisoning manipulates which documents get retrieved, so the system gets wrong information even without any hidden instruction. Prompt injection manipulates the model's behavior through instructions in the text.
2. Other tenants' data never becomes a candidate, so a forgotten filter in some code path can't leak it, and the user still gets a full set of relevant results.
3. Research shows text can be partly reconstructed from embeddings, so a leaked vector store can leak the underlying content.

</details>

## Go deeper

- [OWASP LLM08:2025 Vector and embedding weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) - Official entry. *Beginner · Standard · 15 min*
- [Text Embeddings Reveal (Almost) As Much As Text](https://arxiv.org/abs/2310.06816) - The embedding inversion research. *Intermediate · Paper · 30 min*
- [pgvector](https://github.com/pgvector/pgvector) - Vector search inside PostgreSQL, where row-level security can enforce tenant filters. *Intermediate · Docs · 20 min*
