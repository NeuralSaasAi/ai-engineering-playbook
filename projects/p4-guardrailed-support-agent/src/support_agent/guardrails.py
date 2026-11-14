"""Input and output guardrails (see 03-ai-safety-guardrails/).

Each check returns a `Verdict`. Cheap checks run first. The agent stops at the first block.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from support_agent import pii

MAX_INPUT_CHARS = 2_000


@dataclass
class Verdict:
    allowed: bool
    text: str
    reasons: list[str] = field(default_factory=list)


# --- input -------------------------------------------------------------------------------------------

INJECTION = [
    re.compile(r"\bignore (all |any |your )?(previous |prior |above )?(instructions|rules)\b", re.I),
    re.compile(r"\b(system prompt|developer message|your instructions)\b", re.I),
    re.compile(r"\byou are (now )?(dan|in developer mode|unrestricted)\b", re.I),
    re.compile(r"\b(pretend|act as|role-?play)\b.{0,40}\b(no rules|unfiltered|without restrictions)\b", re.I),
    re.compile(r"\bdo anything now\b", re.I),
]
ON_TOPIC = re.compile(
    r"\b(order|orders|refund|return|returns|deliver\w*|ship\w*|track\w*|parcel|package|payment|paid|"
    r"charged|invoice|cancel\w*|exchange|damaged|broken|wrong item|account|hello|hi|help|thanks|thank you)\b",
    re.I,
)


def check_input(message: str) -> Verdict:
    if not message.strip():
        return Verdict(False, message, ["empty message"])
    if len(message) > MAX_INPUT_CHARS:
        return Verdict(False, message, [f"message too long ({len(message)} > {MAX_INPUT_CHARS} chars)"])
    if any(p.search(message) for p in INJECTION):
        return Verdict(False, message, ["possible prompt injection or jailbreak"])
    if not ON_TOPIC.search(message):
        return Verdict(False, message, ["off topic"])
    found = pii.find(message)
    redacted = pii.redact(message) if found else message
    return Verdict(True, redacted, [f"redacted {t}" for t in found])


# --- output ------------------------------------------------------------------------------------------

COMMITMENTS = re.compile(
    r"\b(i guarantee|guaranteed|i promise|you will definitely|refund (is|has been) approved|"
    r"we will compensate|legally)\b",
    re.I,
)
URL = re.compile(r"https?://([^/\s)]+)")
ALLOWED_DOMAINS = {"shop.example", "help.shop.example"}


def check_output(reply: str) -> Verdict:
    reasons = []
    if found := pii.find(reply):
        reasons.append(f"reply contains PII: {', '.join(found)}")
    if COMMITMENTS.search(reply):
        reasons.append("reply makes a commitment only a human can make")
    for host in URL.findall(reply):
        if host.lower() not in ALLOWED_DOMAINS:
            reasons.append(f"reply links to unapproved domain {host}")
    return Verdict(not reasons, reply, reasons)


SAFE_FALLBACK = (
    "Sorry, I can't help with that here. I can check order status, explain our return policy, "
    "or pass a refund request to our team."
)
