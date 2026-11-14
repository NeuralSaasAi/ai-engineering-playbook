# 06 · Agent memory

Agents fail in two opposite ways: they forget what matters, or they remember the wrong thing and keep acting on it. This module covers how memory works and how to keep it accurate, safe and private.

**You'll be able to:** design short-term and long-term memory for an agent, defend memory writes against poisoning, and build memory features that respect user privacy and the law.

| # | Note | Level | Time |
|---|---|---|---|
| 1 | [How agents remember](memory-types.md) | Beginner | 10 min |
| 2 | [Memory poisoning](memory-poisoning.md) | Intermediate | 10 min |
| 3 | [Memory and privacy](memory-privacy.md) | Beginner | 10 min |

**Related:** [Context and memory files for coding agents](../01-coding-agents/context-and-memory-files.md) covers the same ideas from the coding-agent side.

**Project:** [P3 · LangGraph research agent](../projects/p3-langgraph-research-agent/README.md) uses a checkpointer for short-term memory, a per-user store for long-term memory, and human approval before anything is saved.

**Next:** [07 · Agent ops and production](../07-agent-ops-production/README.md)
