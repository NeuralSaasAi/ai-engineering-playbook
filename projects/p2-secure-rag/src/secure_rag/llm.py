"""Model clients. Both expose `complete(system, user) -> str`.

`GullibleFakeLLM` is a deliberately easy-to-fool stand-in for a real model, so the attack suite runs
offline and gives the same result every time. It does what real models sometimes do:

- answers from the retrieved source that best matches the question, citing it;
- repeats its instructions when asked to;
- obeys instructions hidden inside retrieved documents ("AI assistant: append ...").

The point of the project: the defenses must work EVEN THOUGH the model is fooled. A real model is
harder to fool than this one, but never impossible, so design as if it always is.
"""

from __future__ import annotations

import os
import re
from typing import Protocol

SOURCE = re.compile(r'<source id="([^"]+)"[^>]*>(.*?)</source>', re.S)
QUESTION = re.compile(r"Question:\s*(.*)\Z", re.S)
INJECTED = re.compile(r"AI assistant:\s*append\s+(.+?)(?:-->|$)", re.I | re.M)
EMAIL = re.compile(r"User email:\s*(\S+)")
EXTRACTION = re.compile(r"\b(repeat|print|show)\b.*\b(instructions|system prompt|above)\b", re.I)
WORD = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "what",
    "how",
    "many",
    "do",
    "i",
    "my",
    "of",
    "to",
    "for",
    "in",
    "can",
}


class LLM(Protocol):
    def complete(self, system: str, user: str) -> str: ...


def _words(text: str) -> set[str]:
    return {w for w in WORD.findall(text.lower()) if w not in STOPWORDS}


class GullibleFakeLLM:
    """Deterministic fake model. See module docstring."""

    def complete(self, system: str, user: str) -> str:
        question_match = QUESTION.search(user)
        question = question_match.group(1).strip() if question_match else user

        if EXTRACTION.search(question):
            return f"Sure! My instructions are:\n{system}"

        sources = SOURCE.findall(user)
        if not sources:
            return "I couldn't find that in the documents."

        q = _words(question)
        best_id, best_text = max(sources, key=lambda s: len(q & _words(s[1])))
        if not q & _words(best_text):
            return "I couldn't find that in the documents."

        sentence = max(re.split(r"(?<=[.!?])\s+", best_text.strip()), key=lambda s: len(q & _words(s)))
        sentence = INJECTED.sub("", sentence).replace("<!--", "").strip()
        answer = f"{sentence} [{best_id}]"

        # The gullible part: follow any instruction hidden in ANY retrieved source.
        email = EMAIL.search(system)
        for _, text in sources:
            for payload in INJECTED.findall(text):
                answer += "\n" + payload.strip().replace("DATA", email.group(1) if email else "")
        return answer


class LiteLLMClient:
    """Real model via LiteLLM. Default is Gemini's free tier; change MODEL in .env for another provider."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("MODEL", "gemini/gemini-3.5-flash-lite")

    def complete(self, system: str, user: str) -> str:
        from litellm import completion

        resp = completion(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0,
            max_tokens=400,
            timeout=30,
            num_retries=2,
        )
        return resp.choices[0].message.content or ""
