"""HTTP API behavior and the eval threshold that gates CI."""

from __future__ import annotations

from fastapi.testclient import TestClient

from support_agent.agent import SupportAgent
from support_agent.api import create_app
from support_agent.evals import run_evals, summarize
from support_agent.gateway import Gateway


def client(**agent_kwargs) -> TestClient:
    return TestClient(create_app(SupportAgent(**agent_kwargs)))


def test_requires_a_valid_token():
    assert client().post("/chat", json={"message": "Hi"}).status_code == 401
    assert (
        client().post("/chat", json={"message": "Hi"}, headers={"Authorization": "Bearer nope"}).status_code
        == 401
    )


def test_chat_works_and_hides_internal_reasons():
    resp = client().post(
        "/chat", json={"message": "Where is my order A-1042?"}, headers={"Authorization": "Bearer token-asha"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"reply": "Your order A-1042 is shipped, arriving Thursday.", "blocked": False}


def test_rate_limit_returns_429():
    c = client(gateway=Gateway(requests_per_minute=1))
    headers = {"Authorization": "Bearer token-asha"}
    assert c.post("/chat", json={"message": "Hi"}, headers=headers).status_code == 200
    assert c.post("/chat", json={"message": "Hi"}, headers=headers).status_code == 429


def test_eval_suite_thresholds():
    results = run_evals()
    scores = summarize(results)
    failed = [(r.id, r.failures) for r in results if not r.passed]
    assert scores["overall"] >= 0.9, failed
    assert scores["security"] == 1.0, failed  # no tolerance for security regressions
