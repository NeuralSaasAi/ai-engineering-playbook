"""MkDocs hooks that let the same markdown work on GitHub and on the website.

Nothing in the notes needs to change for the site. This file:

1. Builds the navigation from the module README tables, so there's no second list to maintain.
2. Rewrites links to non-page files (code, data, Dockerfiles) to their GitHub URLs.
3. Lets markdown inside <details> render on the site, as it does on GitHub.
4. Adds a level / last-reviewed line under each note's title, from its front matter.
5. Uses the home template for the root README.
6. Writes robots.txt pointing at the sitemap.
"""

from __future__ import annotations

import datetime as dt
import posixpath
import re
from pathlib import Path

REPO = "https://github.com/NeuralSaasAi/ai-engineering-playbook"
ROOT = Path(__file__).resolve().parent
MODULE_DIR = re.compile(r"^\d\d-[a-z0-9-]+$")
LOCAL_MD_LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)

PROJECTS = [
    "p1-agent-built-cli",
    "p2-secure-rag",
    "p3-langgraph-research-agent",
    "p4-guardrailed-support-agent",
    "p5-production-capstone",
]


def _title(path: Path) -> str:
    m = H1.search(path.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else path.stem


def _module_nav(folder: Path) -> list:
    """Section index first, then pages in the order the README links to them."""
    readme = folder / "README.md"
    entries: list = [{"Overview": f"{folder.name}/README.md"}]
    seen = set()
    for target in LOCAL_MD_LINK.findall(readme.read_text(encoding="utf-8")):
        if "/" in target or target in seen or not (folder / target).exists():
            continue  # only pages inside this module
        seen.add(target)
        entries.append({_title(folder / target): f"{folder.name}/{target}"})
    return entries


def on_config(config, **kwargs):
    modules = sorted(p for p in ROOT.iterdir() if p.is_dir() and MODULE_DIR.match(p.name))
    projects = []
    for name in PROJECTS:
        folder = ROOT / "projects" / name
        items: list = [{"Overview": f"projects/{name}/README.md"}]
        for extra in ("SPEC.md", "AGENTS.md", "REFLECTION.md", "DESIGN.md", "THREAT_MODEL.md"):
            if (folder / extra).exists():
                items.append({_title(folder / extra): f"projects/{name}/{extra}"})
        projects.append({_title(folder / "README.md"): items})

    config["nav"] = [
        {"Home": "README.md"},
        {"Start here": "START-HERE.md"},
        {"Modules": [{_title(m / "README.md"): _module_nav(m)} for m in modules]},
        {"Projects": projects},
        {"Glossary": "glossary.md"},
        {
            "About": [
                {"About this project": "ABOUT.md"},
                {"Progress": "PROGRESS.md"},
                {"Contributing": "CONTRIBUTING.md"},
                {"Style guide": "STYLE.md"},
                {"Code of conduct": "CODE_OF_CONDUCT.md"},
            ]
        },
    ]
    return config


def _rewrite_links(markdown: str, page_src: str, docs_dir: Path, files) -> str:
    """Point links at files that aren't pages (code, data, LICENSE) to GitHub instead."""
    page_dir = posixpath.dirname(page_src)

    def repl(m: re.Match) -> str:
        text, target = m.group(1), m.group(2)
        if re.match(r"^[a-z][a-z0-9+.-]*:|^#", target, re.I):
            return m.group(0)
        path, _, anchor = target.partition("#")
        rel = posixpath.normpath(posixpath.join(page_dir, path))
        full = docs_dir / rel
        page_file = files.get_file_from_path(rel) if path.endswith(".md") else None
        if page_file is not None and not page_file.inclusion.is_excluded():
            return m.group(0)  # a page on the site: MkDocs handles it
        if full.exists():
            kind = "tree" if full.is_dir() else "blob"
            url = f"{REPO}/{kind}/main/{rel}" + (f"#{anchor}" if anchor else "")
            return f"[{text}]({url})"
        return m.group(0)

    return LINK.sub(repl, markdown)


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_uri
    docs_dir = Path(config["docs_dir"])

    if src == "README.md":
        page.meta["template"] = "home.html"
        page.meta["hide"] = ["navigation", "toc"]
        page.meta.setdefault(
            "description",
            "A free playbook for AI engineering in 2027: coding agents, agents, AI safety, "
            "LLM security, evals, memory, production and system design, with hands-on projects.",
        )

    markdown = _rewrite_links(markdown, src, docs_dir, files)
    markdown = re.sub(r"<details>", '<details markdown="1">', markdown)

    level, reviewed = page.meta.get("level"), page.meta.get("last_reviewed")
    if level and reviewed:
        if isinstance(reviewed, str):
            reviewed = dt.date.fromisoformat(reviewed)
        badge = (
            f'<p class="note-meta"><span class="level level-{level}">{str(level).title()}</span>'
            f" · Last reviewed {reviewed:%-d %B %Y}</p>"
        )
        markdown = H1.sub(lambda m: f"{m.group(0)}\n\n{badge}\n", markdown, count=1)
        page.meta.setdefault("description", _first_sentence(markdown))
    return markdown


def _first_sentence(markdown: str) -> str:
    m = re.search(r"^## In one sentence\s*\n+(.+?)\n", markdown, re.M)
    text = re.sub(r"[*`]|\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1)) if m else ""
    return text[:200]


def on_post_build(config, **kwargs):
    site_url = (config.get("site_url") or "").rstrip("/")
    robots = "User-agent: *\nAllow: /\n"
    if site_url:
        robots += f"Sitemap: {site_url}/sitemap.xml\n"
    (Path(config["site_dir"]) / "robots.txt").write_text(robots, encoding="utf-8")
