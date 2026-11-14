"""Chat clients with tool calling. Both return the same shape:

    {"content": str | None, "tool_calls": [{"id", "name", "arguments"}], "usage": {"input", "output"}}

`FakeLLM` is deterministic and deliberately gullible, so guardrail tests mean something offline:
it calls tools for order questions, but it also plays along with jailbreaks and repeats card numbers,
which is exactly what the guardrails must catch.
"""

from __future__ import annotations

import json
import os
import re

ORDER = re.compile(r"\bA-\d{4}\b")
POLICY = (
    "You can return most items within 30 days of delivery. Refunds go back to the original payment "
    "method within 5-7 business days after we receive the item."
)


def _tokens(text: str) -> int:
    return max(1, len(text) // 4)


class FakeLLM:
    def chat(self, messages: list[dict], tools: list[dict]) -> dict:
        last = messages[-1]
        prompt_tokens = sum(_tokens(str(m.get("content") or "")) for m in messages)

        def reply(text: str) -> dict:
            return {
                "content": text,
                "tool_calls": [],
                "usage": {"input": prompt_tokens, "output": _tokens(text)},
            }

        def call(name: str, **args) -> dict:
            tc = {"id": f"call_{len(messages)}", "name": name, "arguments": json.dumps(args)}
            return {"content": None, "tool_calls": [tc], "usage": {"input": prompt_tokens, "output": 20}}

        if last["role"] == "tool":
            data = json.loads(last["content"])
            if "error" in data:
                return reply("I couldn't find that order on your account. Please check the order number.")
            if "ticket" in data:
                return reply(
                    f"I've opened refund request {data['ticket']} for order {data['order_id']}. "
                    "Our team reviews requests within 2 business days."
                )
            return reply(f"Your order {data['order_id']} is {data['status']}.")

        text = str(last["content"])
        low = text.lower()
        if re.search(r"\b(dan|developer mode|no rules|ignore)\b", low):
            return reply("Sure! As DAN, I guarantee you a full refund of 50,000 rupees today.")
        if card := re.search(r"(?:\d[ -]?){15}\d", text):
            return reply(f"Thanks, I've noted your card {card.group()} for the refund.")
        if order := ORDER.search(text):
            if re.search(r"\b(refund|damaged|broken|wrong item|return)\b", low):
                return call("request_refund", order_id=order.group(), reason=text[:200])
            return call("get_order_status", order_id=order.group())
        if "[card]" in low:
            return reply(
                "Please don't share card details here; I've removed them. How can I help with your order?"
            )
        if re.search(r"\b(return|refund)", low):
            return reply(POLICY)
        if re.search(r"\b(hi|hello|help)\b", low):
            return reply("Hi! I can check an order's status, explain returns, or open a refund request.")
        return reply(
            "I can help with orders, deliveries, returns and refunds. What's your order number (like A-1234)?"
        )


class LiteLLMClient:
    """Real model via LiteLLM. Default is Gemini's free tier; set MODEL in .env for another provider."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("MODEL", "gemini/gemini-3.5-flash-lite")

    def chat(self, messages: list[dict], tools: list[dict]) -> dict:
        from litellm import completion

        resp = completion(
            model=self.model,
            messages=messages,
            tools=tools,
            temperature=0,
            max_tokens=400,
            timeout=30,
            num_retries=2,
        )
        msg = resp.choices[0].message
        calls = [
            {"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments}
            for tc in (msg.tool_calls or [])
        ]
        usage = {"input": resp.usage.prompt_tokens, "output": resp.usage.completion_tokens}
        return {"content": msg.content, "tool_calls": calls, "usage": usage}
