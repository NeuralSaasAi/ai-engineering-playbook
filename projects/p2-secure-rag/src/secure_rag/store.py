"""Embeddings and an in-memory vector store.

`HashingEmbedder` turns text into a 512-number vector by hashing words into buckets. It's crude,
but deterministic and offline, which is what tests need. `--live` mode can use a real embedding
model through LiteLLM instead. The store logic is the same either way.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
from dataclasses import dataclass, field

DIMS = 512
WORD = re.compile(r"[a-z0-9]+")


class HashingEmbedder:
    def embed(self, text: str) -> list[float]:
        vec = [0.0] * DIMS
        for word in WORD.findall(text.lower()):
            bucket = int(hashlib.blake2b(word.encode(), digest_size=4).hexdigest(), 16) % DIMS
            vec[bucket] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


class LiteLLMEmbedder:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("EMBEDDING_MODEL", "gemini/gemini-embedding-001")

    def embed(self, text: str) -> list[float]:
        from litellm import embedding

        vec = embedding(model=self.model, input=[text]).data[0]["embedding"]
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)
    vector: list[float] = field(default_factory=list, repr=False)


class VectorStore:
    def __init__(self, embedder) -> None:
        self.embedder = embedder
        self.chunks: list[Chunk] = []

    def add(self, chunk: Chunk) -> None:
        chunk.vector = self.embedder.embed(chunk.text)
        self.chunks.append(chunk)

    def search(self, query: str, top_k: int = 3, where: dict[str, str] | None = None) -> list[Chunk]:
        """Return the top_k most similar chunks.

        `where` filters INSIDE the search, so chunks that don't match are never candidates.
        This is the safe way to do multi-tenant retrieval (see LLM09 in the notes).
        """
        q = self.embedder.embed(query)
        candidates = [
            c for c in self.chunks if not where or all(c.metadata.get(k) == v for k, v in where.items())
        ]
        scored = sorted(candidates, key=lambda c: sum(a * b for a, b in zip(q, c.vector, strict=True)))
        return list(reversed(scored))[:top_k]
