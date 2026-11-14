"""A tiny in-process LLM gateway: per-user rate limits, daily token budgets and usage accounting.

A real deployment would put this in a shared gateway (e.g. the LiteLLM proxy) backed by Redis so
limits hold across many server processes. The logic is the same; see 03-ai-safety-guardrails/llm-gateways.md.
"""

from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class Usage:
    requests: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0


@dataclass
class Gateway:
    requests_per_minute: int = 10
    daily_token_budget: int = 20_000
    # Price per 1M tokens (USD). Placeholder numbers: check your provider's pricing page.
    input_price_per_m: float = 0.10
    output_price_per_m: float = 0.40
    clock: Callable[[], float] = time.monotonic
    _windows: dict[str, deque] = field(default_factory=lambda: defaultdict(deque))
    usage: dict[str, Usage] = field(default_factory=lambda: defaultdict(Usage))

    def check(self, user_id: str) -> str | None:
        """Return a reason to refuse this request, or None to allow it."""
        now = self.clock()
        window = self._windows[user_id]
        while window and now - window[0] >= 60:
            window.popleft()
        if len(window) >= self.requests_per_minute:
            return f"rate limit: {self.requests_per_minute} requests per minute"
        u = self.usage[user_id]
        if u.input_tokens + u.output_tokens >= self.daily_token_budget:
            return f"daily token budget of {self.daily_token_budget} used up"
        window.append(now)
        return None

    def record(self, user_id: str, input_tokens: int, output_tokens: int) -> None:
        u = self.usage[user_id]
        u.requests += 1
        u.input_tokens += input_tokens
        u.output_tokens += output_tokens
        u.cost_usd += (input_tokens * self.input_price_per_m + output_tokens * self.output_price_per_m) / 1e6
