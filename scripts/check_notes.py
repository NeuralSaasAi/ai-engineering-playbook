#!/usr/bin/env python3
"""Check that playbook notes follow the house format.

Rules (see STYLE.md):

Every markdown file in the repo:
  - uses no site-generator-only syntax (MkDocs `!!!` admonitions, Jekyll `{: }` attributes, Liquid `{% %}`)
  - links to other files in this repo with relative paths that exist
  - never links to the published site URL (it changes when the domain moves)
  - links to glossary entries (glossary.md#term) that exist

Every concept note (a .md file inside a numbered module folder, other than README.md):
  - starts with front matter containing title, level (beginner|intermediate) and last_reviewed (YYYY-MM-DD)
  - has the eight template sections, in order, as `## ` headings
  - puts its self-check answers inside <details> blocks
  - stays under the word limit (code blocks and front matter are not counted)
  - defines every **bold term** in its `In one sentence` section in glossary.md

Standard library only, so it runs anywhere with Python 3.10+.
Usage: python3 scripts/check_notes.py [ROOT]
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_SECTIONS = [
    "In one sentence",
    "Why it matters in 2027",
    "Explain it like I'm new",
    "How it works",
    "Example",
    "Common mistakes",
    "Check yourself",
    "Go deeper",
]
LEVELS = {"beginner", "intermediate"}
MAX_WORDS = 1200
MODULE_DIR = re.compile(r"^\d\d-[a-z0-9-]+$")
SKIP_DIRS = {".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache", "site", "fixtures"}
PUBLISHED_SITE = re.compile(r"https?://(neuralsaasai\.github\.io/ai-engineering-playbook|learn\.neuralsaasai\.com)", re.I)
FORBIDDEN_SYNTAX = [
    (re.compile(r"^\s*!!!\s+\w+", re.M), "MkDocs admonition (`!!! note`); use a GitHub alert (`> [!NOTE]`)"),
    (re.compile(r"\{:\s*[.#][^}]*\}"), "Jekyll/kramdown attribute (`{: .class}`)"),
    (re.compile(r"\{%.*?%\}"), "Liquid tag (`{% ... %}`)"),
]
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^(```|~~~).*?^\1\s*$", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]+`")


@dataclass
class Problem:
    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def strip_code(text: str) -> str:
    """Remove fenced and inline code so examples of bad syntax don't trigger errors."""
    text = FENCE.sub("", text)
    return INLINE_CODE.sub("", text)


def split_front_matter(text: str) -> tuple[dict[str, str] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("\"'")
    return meta, text[end + 5 :]


def github_slug(heading: str) -> str:
    """Approximate GitHub's heading anchor rules."""
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug)
    return slug.replace(" ", "-")


def heading_slugs(text: str) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for match in re.finditer(r"^#{1,6}\s+(.+?)\s*#*\s*$", strip_fences_only(text), re.M):
        base = github_slug(match.group(1))
        n = counts.get(base, 0)
        slugs.add(base if n == 0 else f"{base}-{n}")
        counts[base] = n + 1
    return slugs


def strip_fences_only(text: str) -> str:
    return FENCE.sub("", text)


def is_note(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return (
        len(rel.parts) == 2
        and MODULE_DIR.match(rel.parts[0]) is not None
        and rel.name != "README.md"
        and rel.suffix == ".md"
    )


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        rel_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in rel_parts[:-1]):
            continue
        yield path


def check_links(path: Path, text: str, root: Path, slug_cache: dict[Path, set[str]]) -> list[Problem]:
    problems: list[Problem] = []
    for target in LINK.findall(strip_code(text)):
        if PUBLISHED_SITE.match(target):
            problems.append(Problem(path, f"links to the published site ({target}); use a relative .md link"))
            continue
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
            continue  # external (http:, mailto:, ...) - lychee checks these
        file_part, _, anchor = target.partition("#")
        dest = path if not file_part else (path.parent / file_part).resolve()
        if file_part and not dest.exists():
            problems.append(Problem(path, f"broken relative link: {target}"))
            continue
        if file_part.startswith("/"):
            problems.append(Problem(path, f"absolute path link: {target}; use a relative path"))
        if anchor and dest.suffix == ".md":
            if dest not in slug_cache:
                slug_cache[dest] = heading_slugs(dest.read_text(encoding="utf-8"))
            if anchor.lower() not in slug_cache[dest]:
                kind = "glossary entry" if dest.name == "glossary.md" else "heading anchor"
                problems.append(Problem(path, f"missing {kind}: {target}"))
    return problems


def check_note(path: Path, text: str) -> list[Problem]:
    problems: list[Problem] = []
    meta, body = split_front_matter(text)
    if meta is None:
        return [Problem(path, "missing YAML front matter (title, level, last_reviewed)")]
    for key in ("title", "level", "last_reviewed"):
        if not meta.get(key):
            problems.append(Problem(path, f"front matter is missing `{key}`"))
    if meta.get("level") and meta["level"] not in LEVELS:
        problems.append(Problem(path, f"level must be one of {sorted(LEVELS)}, got `{meta['level']}`"))
    if meta.get("last_reviewed"):
        try:
            reviewed = dt.date.fromisoformat(meta["last_reviewed"])
            if reviewed > dt.date.today() + dt.timedelta(days=1):
                problems.append(Problem(path, "last_reviewed is in the future"))
        except ValueError:
            problems.append(Problem(path, "last_reviewed must be YYYY-MM-DD"))

    headings = re.findall(r"^##\s+(.+?)\s*$", strip_fences_only(body), re.M)
    positions = []
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            problems.append(Problem(path, f"missing section `## {section}`"))
        else:
            positions.append(headings.index(section))
    if positions != sorted(positions):
        problems.append(Problem(path, "template sections are out of order (see templates/note-template.md)"))

    check = re.search(r"^## Check yourself\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    if check and "<details>" not in check.group(1):
        problems.append(Problem(path, "`Check yourself` answers must be inside <details> blocks"))

    words = len(re.findall(r"\b\w+\b", strip_code(body)))
    if words > MAX_WORDS:
        problems.append(Problem(path, f"{words} words; split notes longer than {MAX_WORDS} words"))
    return problems


def check_glossary_terms(path: Path, text: str, glossary: set[str]) -> list[Problem]:
    """Bold terms in a note's `In one sentence` section must have a glossary entry."""
    section = re.search(r"^## In one sentence\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not section:
        return []
    problems = []
    for term in re.findall(r"\*\*([^*]+)\*\*", strip_code(section.group(1))):
        slug = github_slug(term)
        candidates = {slug, slug.rstrip("s"), re.sub(r"ies$", "y", slug)}
        if not candidates & glossary:
            problems.append(Problem(path, f"bold term `{term}` has no entry in glossary.md"))
    return problems


def check_repo(root: Path) -> list[Problem]:
    root = root.resolve()
    problems: list[Problem] = []
    slug_cache: dict[Path, set[str]] = {}
    glossary_path = root / "glossary.md"
    glossary = heading_slugs(glossary_path.read_text(encoding="utf-8")) if glossary_path.exists() else set()
    for path in iter_markdown(root):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root)
        for pattern, label in FORBIDDEN_SYNTAX:
            if pattern.search(strip_code(text)):
                problems.append(Problem(rel, f"site-only syntax found: {label}"))
        problems += [Problem(rel, p.message) for p in check_links(path, text, root, slug_cache)]
        if is_note(path, root):
            problems += [Problem(rel, p.message) for p in check_note(path, text)]
            problems += check_glossary_terms(rel, text, glossary)
    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    problems = check_repo(root)
    for problem in problems:
        print(problem)
    notes = sum(1 for p in iter_markdown(root.resolve()) if is_note(p, root.resolve()))
    if problems:
        print(f"\n{len(problems)} problem(s) found.")
        return 1
    print(f"OK: {notes} notes checked, no problems found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
