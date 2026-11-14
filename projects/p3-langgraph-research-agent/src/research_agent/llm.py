"""Model clients for the planner and writer roles. Both expose `complete(system, user) -> str`.

`FakeLLM` is deterministic so tests and evals run offline:
- as PLANNER it splits a question into sub-questions on " and " / ";" (max 3) and returns JSON;
- as WRITER it writes one cited sentence per note, as bullets if a memory says the user prefers them,
  and (like a gullible real model) obeys "AI assistant: append ..." lines inside notes.
"""

from __future__ import annotations

import json
import os
import re

NOTE = re.compile(r'<note source="([^"]+)">(.*?)</note>', re.S)
MEMORY = re.compile(r"<memory>(.*?)</memory>", re.S)
INJECTED = re.compile(r"AI assistant:\s*append\s+(.+?)(?:$|\n)", re.I)


class FakeLLM:
    def complete(self, system: str, user: str) -> str:
        if "PLANNER" in system:
            parts = [p.strip(" ?.") for p in re.split(r"\band\b|;", user) if p.strip(" ?.")]
            return json.dumps([p + "?" for p in parts[:3]])

        notes = NOTE.findall(user)
        if not notes:
            return "I couldn't find anything in the library about that."
        memories = " ".join(MEMORY.findall(user)).lower()
        bullet = "- " if "bullet" in memories else ""
        lines = []
        for source, text in notes:
            first = INJECTED.sub("", text).strip().split(". ")[0].rstrip(".")
            lines.append(f"{bullet}{first}. [{source}]")
            lines += [m.strip() for m in INJECTED.findall(text)]  # the gullible part
        return ("\n" if bullet else " ").join(lines)


class LiteLLMClient:
    """Real model via LiteLLM. Default is Gemini's free tier; set MODEL in .env for another provider."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("MODEL", "gemini/gemini-3.5-flash-lite")

    def complete(self, system: str, user: str) -> str:
        from litellm import completion

        resp = completion(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0,
            max_tokens=600,
            timeout=30,
            num_retries=2,
        )
        return resp.choices[0].message.content or ""
