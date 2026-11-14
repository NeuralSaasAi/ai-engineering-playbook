"""Tools the support agent may call. Each one enforces its own permissions (action guardrails).

The model never chooses WHO the user is: `user_id` comes from the authenticated session.
Refunds are never issued by the agent; it can only open a request that a person approves.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

ORDER_ID = re.compile(r"^A-\d{4}$")

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get the delivery status of one of the CURRENT user's orders. Use when they ask "
            "where an order is or when it will arrive.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string", "pattern": "^A-\\d{4}$"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_refund",
            "description": "Open a refund request for a human to review, for one of the CURRENT user's "
            "orders. This does NOT issue a refund.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "pattern": "^A-\\d{4}$"},
                    "reason": {"type": "string", "maxLength": 200},
                },
                "required": ["order_id", "reason"],
            },
        },
    },
]


@dataclass
class Shop:
    orders: dict[str, dict] = field(
        default_factory=lambda: {
            "A-1042": {"owner": "u-asha", "status": "shipped, arriving Thursday", "total_inr": 2499},
            "A-1043": {"owner": "u-asha", "status": "delivered on 2 Nov", "total_inr": 899},
            "A-2001": {"owner": "u-vikram", "status": "processing", "total_inr": 15999},
        }
    )
    refund_queue: list[dict] = field(default_factory=list)

    def _own_order(self, order_id: str, user_id: str) -> dict | None:
        if not ORDER_ID.match(order_id or ""):
            return None
        order = self.orders.get(order_id)
        return order if order and order["owner"] == user_id else None  # same answer: no existence leak

    def get_order_status(self, user_id: str, order_id: str) -> dict:
        order = self._own_order(order_id, user_id)
        return {"order_id": order_id, "status": order["status"]} if order else {"error": "order not found"}

    def request_refund(self, user_id: str, order_id: str, reason: str) -> dict:
        order = self._own_order(order_id, user_id)
        if not order:
            return {"error": "order not found"}
        ticket = {
            "ticket": f"R-{len(self.refund_queue) + 1:04d}",
            "order_id": order_id,
            "reason": reason[:200],
        }
        self.refund_queue.append({**ticket, "user_id": user_id, "status": "pending human review"})
        return {**ticket, "status": "pending human review"}

    def call(self, name: str, arguments: str, user_id: str) -> str:
        """Dispatch a model's tool call. Unknown tools and bad arguments are refused, not crashed on."""
        try:
            args = json.loads(arguments or "{}")
        except json.JSONDecodeError:
            return json.dumps({"error": "arguments were not valid JSON"})
        if name == "get_order_status":
            return json.dumps(self.get_order_status(user_id, str(args.get("order_id", ""))))
        if name == "request_refund":
            result = self.request_refund(user_id, str(args.get("order_id", "")), str(args.get("reason", "")))
            return json.dumps(result)
        return json.dumps({"error": f"unknown tool {name}"})
