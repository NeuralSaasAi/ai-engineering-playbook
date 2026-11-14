# Glossary

Every term the playbook defines, in one or two plain sentences, with a link to where it's explained. Alphabetical.

## A

### Agent

An LLM running in a loop: it decides the next action (usually a tool call), sees the result, and repeats until it can answer or hits a limit. See [the agent loop](02-building-agents/the-agent-loop.md).

### Agent memory

Everything an agent can draw on beyond the current request, split into short-term and long-term memory. See [how agents remember](06-agent-memory/memory-types.md).

### Agentic SDLC

A software development workflow where you write specs, plans, tests and reviews and a coding agent does most of the typing: spec, plan, tests first, implement, verify, review. See [the new workflow](01-coding-agents/agentic-sdlc.md).

### AI compliance

Building AI systems that meet the laws and standards that apply to them, such as India's DPDP Act, the GDPR and the EU AI Act, and keeping records that prove it. See [compliance basics](08-ai-system-design/compliance-basics.md).

### AI system design

Deciding how an AI product's parts fit together and making explicit trade-offs between quality, cost, latency, safety and simplicity. See [fundamentals](08-ai-system-design/design-fundamentals.md).

### API

Application programming interface: the way one program asks another for something. For LLMs, your code sends messages over HTTPS and gets the reply back. See [calling an LLM](00-foundations/calling-an-llm-api.md).

## C

### Checkpointer

A LangGraph component that saves the graph's state after every step under a thread ID, enabling conversation memory, resuming and human approval. See [LangGraph basics](02-building-agents/langgraph-basics.md).

### Coding agent

An LLM that acts on your project (reads files, runs commands, edits code, runs tests) in a loop until a task is done. See [what is a coding agent?](01-coding-agents/what-is-a-coding-agent.md).

### Context window

The maximum number of tokens a model can consider in one request, covering instructions, history, documents and its own output. See [tokens and context windows](00-foundations/tokens-and-context-windows.md).

## D

### Data poisoning

Tampering with the data a model learns from or retrieves so it behaves the way an attacker wants. OWASP LLM05:2026. See [poisoning](04-llm-security/data-and-model-poisoning.md).

## E

### Edge

In LangGraph, a connection that decides which node runs next. A conditional edge chooses based on the state. See [LangGraph basics](02-building-agents/langgraph-basics.md).

### Embedding

A list of numbers representing the meaning of a piece of text, so that similar meanings get similar numbers. See [embeddings](00-foundations/embeddings.md).

### Eval

A repeatable test that runs an AI system on fixed inputs and scores the outputs. See [why evals](05-evaluation/why-evals.md).

### Excessive agency

Giving an LLM system more tools, permissions or autonomy than its job needs. OWASP LLM03:2026. See [excessive agency](04-llm-security/excessive-agency.md).

## G

### Generation metrics

Measures of a RAG answer's quality, such as faithfulness to sources and relevance to the question. See [RAG metrics](05-evaluation/rag-metrics.md).

### Golden dataset

A small, expert-reviewed set of test inputs with expected behavior, run against every version of a system. See [golden datasets](05-evaluation/golden-datasets.md).

### Guardrail

A check around an LLM, on input, output or actions, that blocks or fixes unsafe, off-topic, private or malformed content. See [what are guardrails?](03-ai-safety-guardrails/what-are-guardrails.md).

## H

### Hallucination

Fluent, confident model output that is false or unsupported. See [how LLMs work](00-foundations/how-llms-work.md).

### Hidden context exposure

Extraction of context users aren't meant to see (system prompt, tool schemas, retrieved rules), which matters when it holds secrets or security logic. OWASP LLM08:2026, formerly system prompt leakage. See [hidden context exposure](04-llm-security/hidden-context-exposure.md).

### Hook

A script that runs automatically at a fixed point in an agent's lifecycle (before a tool runs, when the agent stops) to check or enforce something. See [subagents and hooks](01-coding-agents/subagents-and-hooks.md).

### Human-in-the-loop

An agent pausing before a risky action so a person can approve, edit or reject it. See [human-in-the-loop](02-building-agents/human-in-the-loop.md).

## I

### Improper output handling

Passing model output to another system (browser, database, shell) without validating or encoding it. OWASP LLM10:2026. See [improper output handling](04-llm-security/improper-output-handling.md).

## J

### Jailbreak

A prompt designed to make a model break its own safety rules. A form of prompt injection. See [jailbreaks](03-ai-safety-guardrails/jailbreaks.md).

## L

### LangGraph

An open-source framework that models an agent as a graph of nodes, edges and shared state, with checkpointing. See [LangGraph basics](02-building-agents/langgraph-basics.md).

### Large language model

A program trained on huge amounts of text to predict the next token, repeatedly, which lets it write answers, code and more. Usually shortened to LLM. See [how LLMs work](00-foundations/how-llms-work.md).

### LLM gateway

A proxy between your apps and model providers that enforces keys, budgets, rate limits, guardrails and logging in one place. See [LLM gateways](03-ai-safety-guardrails/llm-gateways.md).

### LLM-as-a-judge

Using a model with a rubric to score another system's outputs on qualities code can't check. See [LLM-as-a-judge](05-evaluation/llm-as-judge.md).

### Long-term memory

Facts, preferences and past experiences an agent saves across sessions and retrieves when relevant. See [how agents remember](06-agent-memory/memory-types.md).

## M

### Memory file

A markdown file such as `AGENTS.md` or `CLAUDE.md` that a coding agent reads at the start of every session. See [memory files](01-coding-agents/context-and-memory-files.md).

### Memory poisoning

Getting false information or hidden instructions saved into an agent's long-term memory. OWASP ASI06. See [memory poisoning](06-agent-memory/memory-poisoning.md).

### Misinformation

Wrong or unsupported model output that looks credible enough to be acted on. OWASP LLM07:2026. See [misinformation](04-llm-security/misinformation.md).

### MITRE ATLAS

A public catalog of attacker tactics and techniques against AI systems, with case studies. See [frameworks](04-llm-security/frameworks-atlas-nist.md).

### Model Context Protocol

An open standard (MCP) for connecting AI applications to outside tools and data through MCP servers. See [MCP](01-coding-agents/mcp.md).

### Multi-agent system

Several specialized agents coordinated by a supervisor, a pipeline or handoffs. See [multi-agent patterns](02-building-agents/multi-agent-patterns.md).

## N

### NIST AI Risk Management Framework

A voluntary US framework for managing AI risk through four functions: Govern, Map, Measure, Manage. See [frameworks](04-llm-security/frameworks-atlas-nist.md).

### Node

In LangGraph, one step in the graph: a function that reads the state and returns updates. See [LangGraph basics](02-building-agents/langgraph-basics.md).

## O

### Observability

Recording what happens inside every request as connected traces, so you can explain, debug and monitor an AI system. See [observability](07-agent-ops-production/observability-and-tracing.md).

### OWASP Top 10 for Agentic Applications

OWASP's list of the ten biggest security risks for agents (ASI01 to ASI10), published December 2025. See [agentic threats](04-llm-security/agentic-threats.md).

## P

### Personal data

Any information about an identifiable person. Data-protection laws such as DPDP and GDPR govern how it's handled. See [memory and privacy](06-agent-memory/memory-privacy.md).

### PII

Personally identifiable information, such as names, phone numbers, emails, Aadhaar, PAN or card numbers. See [PII and privacy](03-ai-safety-guardrails/pii-and-privacy.md).

### Prompt

The text you send to an LLM, usually split into system, user, assistant and tool messages. See [prompting basics](00-foundations/prompting-basics.md).

### Prompt injection

Text the model reads (from a user, a document, a web page or a tool) changing its behavior in ways the developer didn't intend. OWASP LLM01:2026. See [prompt injection](04-llm-security/prompt-injection.md).

## R

### Red-teaming

Deliberately attacking your own AI system, manually and with tools, to find weaknesses before attackers do. See [red-teaming](05-evaluation/red-teaming.md).

### Reliability

Keeping acceptable answers flowing despite slow or failing providers, traffic spikes and step failures. See [reliability and scaling](07-agent-ops-production/reliability-and-scaling.md).

### Retrieval metrics

Measures of whether a RAG system found the right chunks: hit rate, recall, precision, MRR. See [RAG metrics](05-evaluation/rag-metrics.md).

### Retrieval-augmented generation

Finding relevant passages in your documents and putting them in the prompt so the model answers from them. Usually shortened to RAG. See [RAG in one page](00-foundations/rag-in-one-page.md).

## S

### Sensitive information disclosure

An LLM system exposing data someone didn't authorize, through answers, tools, logs or retrieval. OWASP LLM02:2026. See [sensitive information disclosure](04-llm-security/sensitive-information-disclosure.md).

### Short-term memory

The state of the current conversation or task, held in the context window and a checkpointer. See [how agents remember](06-agent-memory/memory-types.md).

### Skill

A folder with a `SKILL.md` file that teaches an agent one task, loaded only when needed. See [skills](01-coding-agents/skills.md).

### State

In LangGraph, the shared data passed between nodes and saved by the checkpointer. See [LangGraph basics](02-building-agents/langgraph-basics.md).

### Subagent

A helper agent with its own fresh context and limited tools, handed a focused job by a main agent. See [subagents and hooks](01-coding-agents/subagents-and-hooks.md).

### Supply chain

Everything your system depends on from outside: models, adapters, datasets, packages, MCP servers, skills. OWASP LLM04:2026. See [supply chain](04-llm-security/supply-chain.md).

## T

### Temperature

A setting that controls how random the model's choice of next token is. Low means more predictable. See [how LLMs work](00-foundations/how-llms-work.md).

### Threat modeling

A structured way to work out what could go wrong with a system and what to do about it, before attackers do. See [threat modeling](08-ai-system-design/threat-modeling.md).

### Token

A chunk of text (a word or part of one) that a model reads and writes. Pricing and limits are counted in tokens. See [tokens](00-foundations/tokens-and-context-windows.md).

### Tool calling

Describing functions to a model so it can request calls with structured arguments, which your code validates and runs. See [tool calling](02-building-agents/tool-calling.md).

### Trace

The connected record of every step (spans) in one request, such as model calls, tool calls and guardrail checks. See [observability](07-agent-ops-production/observability-and-tracing.md).

## U

### Unbounded consumption

No effective limits on usage, letting attackers run up bills, cause outages or copy model behavior. OWASP LLM06:2026. See [unbounded consumption](04-llm-security/unbounded-consumption.md).

## V

### Vector and embedding weaknesses

Security problems in similarity search, such as cross-tenant leaks, retrieval poisoning and embedding inversion. OWASP LLM09:2026. See [vector weaknesses](04-llm-security/vector-and-embedding-weaknesses.md).

### Vector search

Finding stored texts whose embeddings are closest to a query's embedding. See [embeddings](00-foundations/embeddings.md).

## W

### Workflow

A fixed sequence of LLM calls and code, where your code, not the model, controls the order of steps. See [when not to use an agent](02-building-agents/when-not-to-use-agents.md).
