"""Run every code block in the notes that is marked as runnable offline.

A Python code fence whose first line is `# test: run` must execute without errors and without
network access or API keys. This keeps examples correct as libraries change.

Run: uv run --with pytest --with langgraph pytest scripts/tests/test_snippets.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FENCE = re.compile(r"^```python\n(# test: run\n.*?)^```", re.M | re.S)


def collect() -> list[tuple[str, str]]:
    snippets = []
    for path in sorted(ROOT.glob("[0-9][0-9]-*/*.md")):
        for i, match in enumerate(FENCE.finditer(path.read_text(encoding="utf-8"))):
            snippets.append((f"{path.relative_to(ROOT)}#{i + 1}", match.group(1)))
    return snippets


SNIPPETS = collect()


def test_snippets_were_found():
    assert SNIPPETS, "expected at least one `# test: run` snippet in the notes"


@pytest.mark.parametrize(("name", "code"), SNIPPETS, ids=[n for n, _ in SNIPPETS])
def test_snippet_runs(name, code, tmp_path):
    script = tmp_path / "snippet.py"
    script.write_text(code, encoding="utf-8")
    env = {"PATH": "/usr/bin:/bin", "PYTHONIOENCODING": "utf-8"}  # no API keys available
    result = subprocess.run(  # noqa: S603
        [sys.executable, str(script)], capture_output=True, text=True, timeout=60, env=env, cwd=tmp_path
    )
    assert result.returncode == 0, f"{name} failed:\n{result.stderr}"
