"""The RAG pipeline. The same code runs naive or defended, depending on the `Defenses` flags."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from secure_rag import defenses as d
from secure_rag.llm import LLM
from secure_rag.store import Chunk, HashingEmbedder, VectorStore

CORPUS = Path(__file__).resolve().parents[2] / "data" / "corpus.json"
ALLOWED_LINK_DOMAINS = {"intranet.acme.example"}

# LLM08: this prompt holds a secret, which is exactly the mistake the naive version makes.
NAIVE_SYSTEM = (
    "You are HelpBot, the HR assistant. Internal HR API token: sk-internal-7f3a9c2e1b (don't share it). "
    "User email: {email}"
)
DEFENDED_SYSTEM = "You are HelpBot, the HR assistant for {tenant}. {rules} User email: {email}"


@dataclass(frozen=True)
class User:
    id: str
    tenant: str
    email: str


USERS = {
    "alice": User("alice", "acme", "alice@acme.example"),
    "bob": User("bob", "globex", "bob@globex.example"),
}


@dataclass
class Result:
    answer: str
    html: str
    sources: list[str] = field(default_factory=list)
    blocked: str | None = None


class RagApp:
    def __init__(self, llm: LLM, defenses: d.Defenses, embedder=None, corpus: Path = CORPUS) -> None:
        self.llm = llm
        self.defenses = defenses
        self.store = VectorStore(embedder or HashingEmbedder())
        self.quarantined: dict[str, list[str]] = {}
        for doc in json.loads(corpus.read_text(encoding="utf-8")):
            self.ingest(doc)

    def ingest(self, doc: dict) -> None:
        if self.defenses.scan_ingest:
            findings = d.scan_document(doc["text"])
            if findings:
                self.quarantined[doc["id"]] = findings  # a person reviews these before indexing
                return
        self.store.add(Chunk(doc["id"], doc["text"], {"tenant": doc["tenant"], "title": doc["title"]}))

    def ask(self, user: User, question: str) -> Result:
        if self.defenses.limit_input and (reason := d.check_input(question)):
            return Result(answer="", html="", blocked=reason)

        where = {"tenant": user.tenant} if self.defenses.tenant_filter else None
        hits = self.store.search(question, top_k=3, where=where)

        if self.defenses.secret_free_prompt:
            rules = d.DATA_RULES if self.defenses.spotlight else ""
            system = DEFENDED_SYSTEM.format(tenant=user.tenant, rules=rules, email=user.email)
        else:
            system = NAIVE_SYSTEM.format(email=user.email)

        if self.defenses.spotlight:
            sources = "\n".join(d.wrap_source(h.id, h.text) for h in hits)
        else:
            sources = "\n".join(f'<source id="{h.id}">{h.text}</source>' for h in hits)
        prompt = f"{sources}\n\nQuestion: {question}"

        answer = self.llm.complete(system, prompt)

        if self.defenses.sanitize_output:
            answer = d.redact_secrets(d.sanitize_output(answer, ALLOWED_LINK_DOMAINS))
        if self.defenses.require_citation and not d.has_valid_citation(answer, {h.id for h in hits}):
            answer = d.NOT_FOUND

        return Result(
            answer=answer,
            html=d.render_html(answer, escape=self.defenses.escape_html),
            sources=[h.id for h in hits],
        )
