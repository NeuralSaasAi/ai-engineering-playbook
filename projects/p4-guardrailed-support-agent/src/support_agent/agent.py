"""The support agent: gateway -> input guardrails -> model + tools loop -> output guardrails.

┌──────────┐   ┌────────────────┐   ┌──────────────────────┐   ┌─────────────────┐
│ gateway  │ → │ input guards   │ → │ model ⇄ tools        │ → │ output guards   │ → reply
│ rate +   │   │ size, injection│   │ (max 4 steps; tools  │   │ PII, promises,  │
│ budget   │   │ topic, PII mask│   │  check ownership)    │   │ link allowlist  │
└──────────┘   └────────────────┘   └──────────────────────┘   └─────────────────┘
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from support_agent import guardrails
from support_agent.gateway import Gateway
from support_agent.llm import FakeLLM
from support_agent.tools import TOOL_SCHEMAS, Shop

SYSTEM_PROMPT = (
    "You are the customer support assistant for an online shop. You can check the status of the current "
    "user's orders and open refund requests for a human to review. You cannot issue refunds, give "
    "discounts or make promises about outcomes. Keep replies under 80 words. Never ask for card numbers, "
    "OTPs or passwords. If a request is outside orders, deliveries, returns or refunds, "
    "say what you can help with."
)
MAX_STEPS = 4


@dataclass
class Result:
    reply: str
    blocked: bool = False
    reasons: list[str] = field(default_factory=list)
    tool_calls: list[str] = field(default_factory=list)


@dataclass
class SupportAgent:
    llm: object = field(default_factory=FakeLLM)
    shop: Shop = field(default_factory=Shop)
    gateway: Gateway = field(default_factory=Gateway)
    input_guard: bool = True
    output_guard: bool = True

    def respond(self, user_id: str, message: str) -> Result:
        if reason := self.gateway.check(user_id):
            return Result("You're sending messages too quickly. Please wait a minute.", True, [reason])

        text, reasons = message, []
        if self.input_guard:
            verdict = guardrails.check_input(message)
            if not verdict.allowed:
                return Result(guardrails.SAFE_FALLBACK, True, verdict.reasons)
            text, reasons = verdict.text, verdict.reasons

        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}]
        tool_calls: list[str] = []
        reply = ""
        for _ in range(MAX_STEPS):
            out = self.llm.chat(messages, TOOL_SCHEMAS)
            self.gateway.record(user_id, out["usage"]["input"], out["usage"]["output"])
            if not out["tool_calls"]:
                reply = out["content"] or ""
                break
            messages.append(
                {
                    "role": "assistant",
                    "content": out["content"],
                    "tool_calls": [
                        {
                            "id": c["id"],
                            "type": "function",
                            "function": {"name": c["name"], "arguments": c["arguments"]},
                        }
                        for c in out["tool_calls"]
                    ],
                }
            )
            for c in out["tool_calls"]:
                tool_calls.append(c["name"])
                result = self.shop.call(c["name"], c["arguments"], user_id)  # user_id from session
                messages.append({"role": "tool", "tool_call_id": c["id"], "content": result})
        else:
            return Result(guardrails.SAFE_FALLBACK, True, ["step limit reached"], tool_calls)

        if self.output_guard:
            verdict = guardrails.check_output(reply)
            if not verdict.allowed:
                return Result(guardrails.SAFE_FALLBACK, True, reasons + verdict.reasons, tool_calls)
        return Result(reply, False, reasons, tool_calls)


def to_json(result: Result) -> str:
    return json.dumps(result.__dict__)
