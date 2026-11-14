"""Interactive demo and eval runner.

uv run research-agent chat            # ask questions; approve or reject memories when asked
uv run research-agent eval            # run the eval set and print a score
add --live to either to use a real model (needs GEMINI_API_KEY or another provider)
"""

from __future__ import annotations

import argparse
import sys
import uuid

from research_agent.evals import run_evals, score
from research_agent.graph import Agent
from research_agent.llm import FakeLLM, LiteLLMClient


def chat(agent: Agent, user_id: str) -> None:
    print(f"Research agent (user: {user_id}).")
    print("Try: 'How long do EV batteries last and how are batteries recycled?'")
    print("Tip: add 'Remember that I prefer bullet points.' to a question. Empty line to quit.\n")
    while question := input("you> ").strip():
        thread = str(uuid.uuid4())  # a new thread per question: long-term memory must carry over
        result = agent.ask(question, user_id=user_id, thread_id=thread)
        print(f"\nagent> {result.get('answer', '')}\n")
        if result.get("blocked_sources"):
            print(f"(ignored suspicious sources: {', '.join(result['blocked_sources'])})")
        if interrupts := result.get("__interrupt__"):
            decision = input(f"{interrupts[0].value['summary']} [approve/reject] ").strip().lower()
            result = agent.resume("approve" if decision.startswith("a") else "reject", user_id, thread)
        if status := result.get("memory_status"):
            if status != "none":
                print(f"(memory: {status})")
        print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="research-agent")
    parser.add_argument("command", choices=["chat", "eval"])
    parser.add_argument("--user", default="demo-user")
    parser.add_argument("--live", action="store_true", help="use a real model through LiteLLM")
    parser.add_argument("--min-score", type=float, default=0.0)
    args = parser.parse_args(argv)

    agent = Agent(llm=LiteLLMClient() if args.live else FakeLLM())
    if args.command == "chat":
        chat(agent, args.user)
        return 0

    results = run_evals(agent)
    for r in results:
        print(("PASS " if r.passed else "FAIL ") + r.id + ("" if r.passed else f"  {r.failures}"))
    s = score(results)
    print(f"\nscore: {s:.0%} ({sum(r.passed for r in results)}/{len(results)})")
    return 0 if s >= args.min_score else 1


if __name__ == "__main__":
    sys.exit(main())
