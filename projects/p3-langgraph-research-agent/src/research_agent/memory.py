"""Long-term memory rules (see 06-agent-memory/memory-poisoning.md).

Only facts the USER states about themselves can become memories, never text from search results.
Every candidate is checked here and then shown to the user for approval before it's saved.
"""

from __future__ import annotations

import re
from datetime import date

# Ends at sentence punctuation followed by a space or the end, so "boss@corp.example" stays whole.
REMEMBER = re.compile(r"\bremember (?:that )?(i .+?)(?:[.!?](?=\s|$)|$)", re.I)
MAX_LEN = 120
FORBIDDEN = [
    re.compile(r"https?://|www\.", re.I),
    re.compile(r"[\w.+-]+@[\w-]+\.\w+"),  # no email addresses: a classic exfiltration target
    re.compile(r"\b(ignore|always send|forward\w*|email\w*|instruction\w*|system prompt)\b", re.I),
]


def namespace(user_id: str) -> tuple[str, str]:
    """One namespace per user, so one user's memories can never reach another user."""
    return ("memories", user_id)


def extract_candidate(user_message: str) -> str | None:
    """Pull out an explicit 'remember that I ...' statement from the user's own message."""
    match = REMEMBER.search(user_message)
    return match.group(1).strip() if match else None


def check_candidate(fact: str) -> str | None:
    """Return a reason to reject the memory, or None if it's acceptable."""
    if len(fact) > MAX_LEN:
        return f"too long ({len(fact)} chars, limit {MAX_LEN})"
    for pattern in FORBIDDEN:
        if pattern.search(fact):
            return "looks like a link, address or instruction, not a preference"
    return None


def record(fact: str, source: str = "user_message") -> dict[str, str]:
    return {"fact": fact, "source": source, "date": date.today().isoformat()}
