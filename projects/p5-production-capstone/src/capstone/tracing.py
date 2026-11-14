"""OpenTelemetry tracing for the P4 agent, without changing P4's code.

Span names and attributes follow the OpenTelemetry GenAI semantic conventions where they exist
(`gen_ai.operation.name`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, ...).

PRIVACY RULE: message and reply text never go into spans. Only lengths, counts, decisions and
token usage do. Traces are often kept longer and read by more people than the data itself.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
from support_agent.agent import Result, SupportAgent
from support_agent.tools import Shop

SERVICE = "support-agent"


def setup_tracing(exporter=None) -> TracerProvider:
    """Send spans to `exporter`, or to OTLP if OTEL_EXPORTER_OTLP_ENDPOINT is set, else to the console."""
    provider = TracerProvider(resource=Resource.create({"service.name": SERVICE}))
    if exporter is not None:
        provider.add_span_processor(SimpleSpanProcessor(exporter))
    elif os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    elif os.environ.get("TRACE_TO_CONSOLE") == "1":
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    return provider


@dataclass
class TracedLLM:
    inner: object
    tracer: trace.Tracer
    model: str = "fake"

    def chat(self, messages: list[dict], tools: list[dict]) -> dict:
        with self.tracer.start_as_current_span(f"chat {self.model}") as span:
            span.set_attribute("gen_ai.operation.name", "chat")
            span.set_attribute("gen_ai.request.model", self.model)
            span.set_attribute("app.messages.count", len(messages))
            out = self.inner.chat(messages, tools)
            span.set_attribute("gen_ai.usage.input_tokens", out["usage"]["input"])
            span.set_attribute("gen_ai.usage.output_tokens", out["usage"]["output"])
            span.set_attribute("app.tool_calls.count", len(out["tool_calls"]))
            return out


class TracedShop(Shop):
    tracer: trace.Tracer

    def call(self, name: str, arguments: str, user_id: str) -> str:
        with self.tracer.start_as_current_span(f"execute_tool {name}") as span:
            span.set_attribute("gen_ai.operation.name", "execute_tool")
            span.set_attribute("gen_ai.tool.name", name)
            result = super().call(name, arguments, user_id)
            span.set_attribute("app.tool.error", '"error"' in result)
            return result


@dataclass
class Metrics:
    latencies_ms: list[float] = field(default_factory=list)
    blocked: int = 0
    requests: int = 0

    def percentile(self, p: float) -> float:
        if not self.latencies_ms:
            return 0.0
        data = sorted(self.latencies_ms)
        return data[min(len(data) - 1, int(round(p / 100 * (len(data) - 1))))]


@dataclass
class ObservedAgent:
    """Wraps a SupportAgent: one root span per request, plus latency and block metrics."""

    agent: SupportAgent
    tracer: trace.Tracer
    metrics: Metrics = field(default_factory=Metrics)

    @classmethod
    def build(cls, provider: TracerProvider, llm=None, model: str = "fake", **agent_kwargs) -> ObservedAgent:
        tracer = provider.get_tracer("capstone")
        shop = TracedShop()
        shop.tracer = tracer
        from support_agent.llm import FakeLLM

        traced_llm = TracedLLM(llm or FakeLLM(), tracer, model)
        return cls(SupportAgent(llm=traced_llm, shop=shop, **agent_kwargs), tracer)

    @property
    def gateway(self):
        return self.agent.gateway

    def respond(self, user_id: str, message: str) -> Result:
        start = time.perf_counter()
        with self.tracer.start_as_current_span("support_request") as span:
            span.set_attribute("app.user.id", user_id)  # a pseudonymous ID, never a name or email
            span.set_attribute("app.input.chars", len(message))
            result = self.agent.respond(user_id, message)
            span.set_attribute("app.blocked", result.blocked)
            span.set_attribute("app.block.reasons", [r.split(":")[0] for r in result.reasons])
            span.set_attribute("app.reply.chars", len(result.reply))
        elapsed = (time.perf_counter() - start) * 1000
        self.metrics.requests += 1
        self.metrics.blocked += result.blocked
        self.metrics.latencies_ms.append(elapsed)
        return result
