"""The agent's only tool: read-only search over a small local library.

Search results are UNTRUSTED. Anyone could have written a forum post in the library, so results are
scanned for instruction-like text before the agent sees them (OWASP LLM01 / ASI01).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

LIBRARY = Path(__file__).resolve().parents[2] / "data" / "library.json"
WORD = re.compile(r"[a-z0-9]+")
STOPWORDS = {"the", "a", "an", "is", "are", "what", "how", "do", "does", "of", "to", "for", "in", "and", "on"}
SUSPICIOUS = [
    re.compile(r"\bAI assistant\s*:", re.I),
    re.compile(r"\bignore (all |any )?(previous|prior) instructions\b", re.I),
    re.compile(r"\b(save|store|remember)\b.{0,40}\bmemory\b", re.I),
    re.compile(r"https?://", re.I),
]


@dataclass(frozen=True)
class Doc:
    id: str
    title: str
    text: str


def words(text: str) -> set[str]:
    return {w for w in WORD.findall(text.lower()) if w not in STOPWORDS}


def load_library(path: Path = LIBRARY) -> list[Doc]:
    return [Doc(**d) for d in json.loads(path.read_text(encoding="utf-8"))]


def is_suspicious(text: str) -> bool:
    return any(p.search(text) for p in SUSPICIOUS)


class SearchTool:
    """Keyword search. Read-only by design: the agent can't change the library."""

    def __init__(self, docs: list[Doc] | None = None) -> None:
        self.docs = docs if docs is not None else load_library()
        self.calls = 0

    def __call__(self, query: str, k: int = 2) -> list[Doc]:
        self.calls += 1
        q = words(query)
        min_overlap = 2 if len(q) >= 2 else 1  # one shared word ("today") is not a match
        scored = [(len(q & words(d.title + " " + d.text)), d) for d in self.docs]
        return [d for score, d in sorted(scored, key=lambda s: -s[0]) if score >= min_overlap][:k]
