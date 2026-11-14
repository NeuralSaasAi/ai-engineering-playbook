# 05 · Evaluation

How to know whether your AI system works, keeps working after changes, and holds up against attacks. Evals are the "tests" of AI engineering.

**You'll be able to:** build a golden dataset, write code-based and LLM-judge graders, measure RAG retrieval and answers separately, and run automated red-team scans.

| # | Note | Level | Time |
|---|---|---|---|
| 1 | [Why evals are the tests of AI](why-evals.md) | Beginner | 10 min |
| 2 | [Building a golden dataset](golden-datasets.md) | Beginner | 10 min |
| 3 | [LLM-as-a-judge](llm-as-judge.md) | Intermediate | 12 min |
| 4 | [Measuring RAG quality](rag-metrics.md) | Intermediate | 12 min |
| 5 | [Red-teaming LLM apps](red-teaming.md) | Intermediate | 12 min |

> [!TIP]
> Design a 10-case eval for any chatbot you use today: 4 common questions, 2 hard ones, 2 out of scope, 2 adversarial. Write what a good answer must and must not include. You've just done the most important part of evaluation.

**Projects:** [P3](../projects/p3-langgraph-research-agent/README.md) and [P4](../projects/p4-guardrailed-support-agent/README.md) both include eval suites that run in CI with minimum scores.

**Next:** [06 · Agent memory](../06-agent-memory/README.md)
