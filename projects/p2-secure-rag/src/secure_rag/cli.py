"""Try the app from the terminal.

uv run secure-rag ask alice "How many unused leave days can be carried over?"
uv run secure-rag ask alice "Can I work from home?" --mode naive
uv run secure-rag attack            # run every attack against both modes and print a table
uv run secure-rag ask alice "..." --live   # use a real model (needs GEMINI_API_KEY or another provider)
"""

from __future__ import annotations

import argparse
import sys

from secure_rag.app import USERS, RagApp
from secure_rag.attacks import ATTACKS
from secure_rag.defenses import DEFENDED, NAIVE
from secure_rag.llm import GullibleFakeLLM, LiteLLMClient


def make_app(mode: str, live: bool) -> RagApp:
    llm = LiteLLMClient() if live else GullibleFakeLLM()
    embedder = None
    if live:
        from secure_rag.store import LiteLLMEmbedder

        embedder = LiteLLMEmbedder()
    return RagApp(llm, DEFENDED if mode == "defended" else NAIVE, embedder=embedder)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="secure-rag")
    sub = parser.add_subparsers(dest="command", required=True)
    ask = sub.add_parser("ask")
    ask.add_argument("user", choices=sorted(USERS))
    ask.add_argument("question")
    ask.add_argument("--mode", choices=["naive", "defended"], default="defended")
    ask.add_argument("--live", action="store_true", help="use a real model through LiteLLM")
    attack = sub.add_parser("attack")
    attack.add_argument("--live", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "ask":
        app = make_app(args.mode, args.live)
        result = app.ask(USERS[args.user], args.question)
        if result.blocked:
            print(f"Blocked: {result.blocked}")
            return 1
        print(result.answer)
        print(f"\n(sources: {', '.join(result.sources)})")
        if app.quarantined:
            print(f"(quarantined at ingestion: {', '.join(app.quarantined)})")
        return 0

    print(f"{'Attack':<42} {'OWASP 2026':<14} {'naive':<12} defended")
    for attack_case in ATTACKS:
        row = []
        for mode in ("naive", "defended"):
            succeeded = attack_case.succeeded(make_app(mode, args.live))
            row.append("BREACHED" if succeeded else "blocked")
        print(f"{attack_case.name:<42} {attack_case.owasp:<14} {row[0]:<12} {row[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
