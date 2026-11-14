"""A small eval runner (see 05-evaluation/why-evals.md). Code-based graders only.

For each case it checks: expected sources were used, every citation points to a note the agent
actually had, required phrases appear, forbidden phrases don't, and memory rules held.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from research_agent.graph import Agent

EVAL_SET = Path(__file__).resolve().parents[2] / "data" / "eval_set.jsonl"
CITATION = re.compile(r"\[([a-z0-9-]+)\]")


@dataclass
class CaseResult:
    id: str
    passed: bool
    failures: list[str]


def grade(case: dict, result: dict) -> list[str]:
    failures = []
    answer = result.get("answer", "")
    used = {n["source"] for n in result.get("notes", [])}
    for src in case.get("expect_sources", []):
        if src not in used:
            failures.append(f"expected source {src} not used")
    for cited in CITATION.findall(answer):
        if cited not in used:
            failures.append(f"cites {cited}, which wasn't in the notes")
    for phrase in case.get("must_include", []):
        if phrase.lower() not in answer.lower():
            failures.append(f"missing '{phrase}'")
    for phrase in case.get("must_not_include", []):
        if phrase.lower() in answer.lower():
            failures.append(f"contains forbidden '{phrase}'")
    if expected := case.get("expect_memory_status"):
        if not str(result.get("memory_status", "")).startswith(expected):
            failures.append(f"memory_status was {result.get('memory_status')!r}, expected {expected!r}")
    return failures


def run_evals(agent: Agent | None = None, path: Path = EVAL_SET) -> list[CaseResult]:
    agent = agent or Agent()
    results = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        out = agent.ask(case["question"], user_id="eval-user", thread_id=f"eval-{case['id']}")
        failures = grade(case, out)
        results.append(CaseResult(case["id"], not failures, failures))
    return results


def score(results: list[CaseResult]) -> float:
    return sum(r.passed for r in results) / len(results)
