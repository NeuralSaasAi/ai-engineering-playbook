"""Eval runner: code-based graders plus an LLM-as-judge grader, reported overall and per tag."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from support_agent.agent import SupportAgent
from support_agent.judge import RuleJudge

EVAL_SET = Path(__file__).resolve().parents[2] / "data" / "eval_set.jsonl"


@dataclass
class CaseResult:
    id: str
    tags: list[str]
    passed: bool
    failures: list[str] = field(default_factory=list)


def load_cases(path: Path = EVAL_SET) -> list[dict]:
    cases = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            case = json.loads(line)
            if "message_repeat" in case:
                text, n = case["message_repeat"]
                case["message"] = text * n
            cases.append(case)
    return cases


def run_evals(agent_factory=SupportAgent, judge=None) -> list[CaseResult]:
    judge = judge or RuleJudge()
    results = []
    for case in load_cases():
        agent = agent_factory()  # fresh agent per case so rate limits don't leak between cases
        out = agent.respond(case["user"], case["message"])
        failures = []
        if out.blocked != case["expect_blocked"]:
            failures.append(f"blocked={out.blocked}, expected {case['expect_blocked']} ({out.reasons})")
        if (tool := case.get("expect_tool")) and tool not in out.tool_calls:
            failures.append(f"expected tool {tool}, got {out.tool_calls}")
        if not case["expect_blocked"]:
            verdict = judge.grade(
                case["message"],
                out.reply,
                case["expected"],
                must_include=case.get("must_include", []),
                must_not_include=case.get("must_not_include", []),
            )
            if verdict["verdict"] != "PASS":
                failures.append(f"judge: {verdict['reasoning']}")
        results.append(CaseResult(case["id"], case["tags"], not failures, failures))
    return results


def summarize(results: list[CaseResult]) -> dict[str, float]:
    by_tag: dict[str, list[bool]] = defaultdict(list)
    for r in results:
        by_tag["overall"].append(r.passed)
        for t in r.tags:
            by_tag[t].append(r.passed)
    return {tag: sum(v) / len(v) for tag, v in sorted(by_tag.items())}
