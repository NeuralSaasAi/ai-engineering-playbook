# Build from the projects/ folder so the P4 dependency is available:
#   docker build -f p5-production-capstone/Dockerfile -t support-agent .
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.1 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1

WORKDIR /app
COPY p4-guardrailed-support-agent /app/p4-guardrailed-support-agent
COPY p5-production-capstone /app/p5-production-capstone
WORKDIR /app/p5-production-capstone
RUN uv sync --locked --no-dev

# Run as a non-root user: if the app is ever compromised, the attacker gets fewer rights.
RUN useradd --create-home --uid 10001 app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz')"
CMD ["/app/p5-production-capstone/.venv/bin/uvicorn", "capstone.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
