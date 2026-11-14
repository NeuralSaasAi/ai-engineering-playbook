"""Try the agent and run evals from the terminal.

uv run support-agent chat [--user u-asha] [--live] [--no-input-guard] [--no-output-guard]
uv run support-agent eval [--live-judge] [--min-score 0.9]
"""

from __future__ import annotations

import argparse
import sys

from support_agent.agent import SupportAgent
from support_agent.evals import run_evals, summarize
from support_agent.judge import LiveJudge, RuleJudge
from support_agent.llm import FakeLLM, LiteLLMClient


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="support-agent")
    parser.add_argument("command", choices=["chat", "eval"])
    parser.add_argument("--user", default="u-asha")
    parser.add_argument("--live", action="store_true", help="real model for the agent")
    parser.add_argument("--live-judge", action="store_true", help="real model as the eval judge")
    parser.add_argument("--no-input-guard", action="store_true")
    parser.add_argument("--no-output-guard", action="store_true")
    parser.add_argument("--min-score", type=float, default=0.0)
    args = parser.parse_args(argv)

    def make_agent() -> SupportAgent:
        return SupportAgent(
            llm=LiteLLMClient() if args.live else FakeLLM(),
            input_guard=not args.no_input_guard,
            output_guard=not args.no_output_guard,
        )

    if args.command == "chat":
        agent = make_agent()
        print("Support agent. Try: 'Where is my order A-1042?'  Empty line to quit.")
        while message := input("you> ").strip():
            r = agent.respond(args.user, message)
            print(f"agent> {r.reply}")
            if r.reasons or r.tool_calls:
                print(f"       (blocked={r.blocked} reasons={r.reasons} tools={r.tool_calls})")
        u = agent.gateway.usage[args.user]
        print(
            f"\nusage: {u.requests} model calls, {u.input_tokens + u.output_tokens} tokens, ${u.cost_usd:.6f}"
        )
        return 0

    results = run_evals(make_agent, LiveJudge() if args.live_judge else RuleJudge())
    for r in results:
        print(("PASS " if r.passed else "FAIL ") + r.id + ("" if r.passed else f"  {r.failures}"))
    scores = summarize(results)
    print("\n" + "\n".join(f"{tag:<12} {s:.0%}" for tag, s in scores.items()))
    return 0 if scores["overall"] >= args.min_score else 1


if __name__ == "__main__":
    sys.exit(main())
