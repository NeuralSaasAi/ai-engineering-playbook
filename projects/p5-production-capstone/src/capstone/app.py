"""Production app: P4's API with tracing, plus a /metrics endpoint for cost and latency.

Run:  uv run uvicorn capstone.app:app
With Jaeger for traces:  docker compose up   (see README)
"""

from __future__ import annotations

import os

from fastapi import FastAPI
from support_agent.api import create_app
from support_agent.gateway import Gateway

from capstone.tracing import ObservedAgent, setup_tracing


def build(provider=None, gateway: Gateway | None = None, live: bool | None = None) -> FastAPI:
    provider = provider or setup_tracing()
    live = os.environ.get("LIVE") == "1" if live is None else live
    llm, model = None, "fake"
    if live:
        from support_agent.llm import LiteLLMClient

        llm = LiteLLMClient()
        model = llm.model
    observed = ObservedAgent.build(provider, llm=llm, model=model, gateway=gateway or Gateway())
    api = create_app(observed)  # P4's routes, auth and limits, unchanged
    api.title = "Support agent (P5, production)"

    @api.get("/metrics")
    def metrics() -> dict:
        m = observed.metrics
        users = {
            uid: {
                "model_calls": u.requests,
                "tokens": u.input_tokens + u.output_tokens,
                "cost_usd": round(u.cost_usd, 6),
            }
            for uid, u in observed.gateway.usage.items()
        }
        return {
            "requests": m.requests,
            "blocked": m.blocked,
            "latency_ms": {"p50": round(m.percentile(50), 2), "p95": round(m.percentile(95), 2)},
            "total_cost_usd": round(sum(u["cost_usd"] for u in users.values()), 6),
            "users": users,
        }

    return api


app = build()
