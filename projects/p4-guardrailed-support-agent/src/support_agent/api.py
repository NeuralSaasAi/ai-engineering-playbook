"""HTTP API. Run: uv run uvicorn support_agent.api:app --reload

POST /chat  with header `Authorization: Bearer <token>` and body {"message": "..."}

The token identifies the user. In a real app this is your login session or an identity provider;
here it's a fixed demo mapping. The model never sees or chooses the user ID.
"""

from __future__ import annotations

import os

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from support_agent.agent import SupportAgent
from support_agent.llm import FakeLLM, LiteLLMClient

DEMO_TOKENS = {"token-asha": "u-asha", "token-vikram": "u-vikram", "token-redteam": "u-redteam"}


class ChatIn(BaseModel):
    message: str = Field(max_length=10_000)


class ChatOut(BaseModel):
    reply: str
    blocked: bool


def current_user(authorization: str = Header(default="")) -> str:
    token = authorization.removeprefix("Bearer ").strip()
    if token not in DEMO_TOKENS:
        raise HTTPException(status_code=401, detail="unknown or missing token")
    return DEMO_TOKENS[token]


def create_app(agent: SupportAgent | None = None) -> FastAPI:
    agent = agent or SupportAgent(llm=LiteLLMClient() if os.environ.get("LIVE") == "1" else FakeLLM())
    api = FastAPI(title="Support agent (P4)")
    api.state.agent = agent

    @api.post("/chat", response_model=ChatOut)
    def chat(body: ChatIn, user_id: str = Depends(current_user)) -> ChatOut:
        result = agent.respond(user_id, body.message)
        if result.reasons and "rate limit" in result.reasons[0]:
            raise HTTPException(status_code=429, detail=result.reply)
        # Reasons are logged server-side, not returned: they would help an attacker tune their input.
        return ChatOut(reply=result.reply, blocked=result.blocked)

    @api.get("/healthz")
    def healthz() -> dict:
        return {"ok": True}

    return api


app = create_app()
