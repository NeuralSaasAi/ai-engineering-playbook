"""PII detection and masking for Indian and common international formats.

Patterns plus checksums (Luhn for cards, Verhoeff for Aadhaar) keep false positives low:
an order number with 16 digits isn't masked unless it passes the card checksum.
For names and addresses you'd add an entity model such as Microsoft Presidio.
"""

from __future__ import annotations

import re

# Verhoeff tables, used by Aadhaar numbers
_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]
_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
    return total % 10 == 0


def verhoeff_ok(digits: str) -> bool:
    c = 0
    for i, ch in enumerate(reversed(digits)):
        c = _D[c][_P[i % 8][int(ch)]]
    return c == 0


CARD = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
AADHAAR = re.compile(r"(?<!\d)[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}(?!\d)")
PATTERNS = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")),
    ("PAN", re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")),
    ("UPI", re.compile(r"\b[\w.-]{2,}@(?:ok\w+|ybl|ibl|axl|paytm|upi)\b", re.I)),
    ("PHONE", re.compile(r"(?<!\d)(?:\+?91[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)")),
]


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s)


def find(text: str) -> list[str]:
    """Return the PII types present in text."""
    found = []
    if any(luhn_ok(_digits(m.group())) for m in CARD.finditer(text)):
        found.append("CARD")
    if any(verhoeff_ok(_digits(m.group())) for m in AADHAAR.finditer(text)):
        found.append("AADHAAR")
    found += [label for label, p in PATTERNS if p.search(text)]
    return found


def redact(text: str) -> str:
    text = CARD.sub(lambda m: "[CARD]" if luhn_ok(_digits(m.group())) else m.group(), text)
    text = AADHAAR.sub(lambda m: "[AADHAAR]" if verhoeff_ok(_digits(m.group())) else m.group(), text)
    for label, pattern in PATTERNS:  # UPI before EMAIL would also work; EMAIL catches most
        text = pattern.sub(f"[{label}]", text)
    return text
