"""Unit tests for scripts/check_notes.py. Run: uv run --with pytest pytest scripts/tests"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_notes  # noqa: E402

GOOD_NOTE = """---
title: What is a token?
level: beginner
last_reviewed: 2026-11-14
---

# What is a token?

## In one sentence

A **token** is a chunk of text the model reads. See the [glossary](../glossary.md#token).

## Why it matters in 2027

Prices are per token.

## Explain it like I'm new

Like syllables.

## How it works

Text is split into pieces.

```text
!!! note this is inside a code block, so it is allowed
```

## Example

"unbelievable" -> "un", "believ", "able".

## Common mistakes

Counting words instead of tokens.

## Check yourself

1. What is a token?

<details><summary>Answer</summary>

A chunk of text.

</details>

## Go deeper

- [Example source](https://example.com) - Beginner, article, 5 min
"""

GLOSSARY = """# Glossary

### Token

A chunk of text.
"""


def make_repo(tmp_path: Path, note: str, glossary: str = GLOSSARY) -> Path:
    (tmp_path / "00-foundations").mkdir()
    (tmp_path / "00-foundations" / "tokens.md").write_text(note)
    (tmp_path / "00-foundations" / "README.md").write_text("# Foundations\n\n- [Tokens](tokens.md)\n")
    (tmp_path / "glossary.md").write_text(glossary)
    return tmp_path


def messages(root: Path) -> list[str]:
    return [p.message for p in check_notes.check_repo(root)]


def test_good_note_passes(tmp_path):
    assert messages(make_repo(tmp_path, GOOD_NOTE)) == []


def test_missing_front_matter(tmp_path):
    note = GOOD_NOTE.split("---\n", 2)[2]
    assert any("front matter" in m for m in messages(make_repo(tmp_path, note)))


def test_bad_level_and_date(tmp_path):
    note = GOOD_NOTE.replace("level: beginner", "level: expert").replace("2026-11-14", "14/11/2026")
    msgs = messages(make_repo(tmp_path, note))
    assert any("level must be" in m for m in msgs)
    assert any("YYYY-MM-DD" in m for m in msgs)


def test_missing_section(tmp_path):
    note = GOOD_NOTE.replace("## Common mistakes", "## Pitfalls")
    assert "missing section `## Common mistakes`" in messages(make_repo(tmp_path, note))


def test_sections_out_of_order(tmp_path):
    note = GOOD_NOTE.replace("## Example", "## TEMP").replace("## How it works", "## Example").replace("## TEMP", "## How it works")
    assert any("out of order" in m for m in messages(make_repo(tmp_path, note)))


def test_answers_must_be_in_details(tmp_path):
    note = GOOD_NOTE.replace("<details><summary>Answer</summary>", "").replace("</details>", "")
    assert any("<details>" in m for m in messages(make_repo(tmp_path, note)))


def test_mkdocs_admonition_outside_code_is_rejected(tmp_path):
    note = GOOD_NOTE.replace("Like syllables.", "!!! note\n    Like syllables.")
    assert any("MkDocs admonition" in m for m in messages(make_repo(tmp_path, note)))


def test_jekyll_attribute_is_rejected(tmp_path):
    note = GOOD_NOTE.replace("Like syllables.", "Like syllables.\n{: .note }")
    assert any("Jekyll" in m for m in messages(make_repo(tmp_path, note)))


def test_broken_relative_link(tmp_path):
    note = GOOD_NOTE.replace("Like syllables.", "See [missing](missing.md).")
    assert "broken relative link: missing.md" in messages(make_repo(tmp_path, note))


def test_missing_glossary_anchor(tmp_path):
    note = GOOD_NOTE.replace("glossary.md#token", "glossary.md#embedding")
    assert any("missing glossary entry" in m for m in messages(make_repo(tmp_path, note)))


def test_published_site_link_rejected(tmp_path):
    note = GOOD_NOTE.replace("https://example.com", "https://neuralsaasai.github.io/ai-engineering-playbook/x/")
    assert any("published site" in m for m in messages(make_repo(tmp_path, note)))


def test_bold_term_needs_glossary_entry(tmp_path):
    note = GOOD_NOTE.replace("A **token**", "A **context window**")
    assert any("context window" in m for m in messages(make_repo(tmp_path, note)))


def test_plural_bold_term_matches_singular_entry(tmp_path):
    note = GOOD_NOTE.replace("A **token**", "**Tokens**")
    assert messages(make_repo(tmp_path, note)) == []


def test_word_limit(tmp_path):
    note = GOOD_NOTE.replace("Like syllables.", "word " * (check_notes.MAX_WORDS + 10))
    assert any("split notes" in m for m in messages(make_repo(tmp_path, note)))


def test_readme_is_not_treated_as_note(tmp_path):
    root = make_repo(tmp_path, GOOD_NOTE)
    assert not check_notes.is_note(root / "00-foundations" / "README.md", root)
    assert check_notes.is_note(root / "00-foundations" / "tokens.md", root)


def test_github_slug():
    assert check_notes.github_slug("Explain it like I'm new") == "explain-it-like-im-new"
    assert check_notes.github_slug("LLM01: Prompt injection") == "llm01-prompt-injection"
