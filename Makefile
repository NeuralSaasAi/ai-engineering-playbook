.PHONY: check notes lint-md test-scripts test-projects links site site-serve

PROJECTS := $(wildcard projects/p*/)

## check: run every offline check (what CI runs, minus the external link check)
check: notes lint-md test-scripts test-projects site

## notes: template, front matter, relative links, glossary, GFM-only syntax
notes:
	python3 scripts/check_notes.py

## lint-md: markdown style
lint-md:
	npx --yes markdownlint-cli2 "**/*.md"

## test-scripts: unit tests for the checker itself
test-scripts:
	uv run --quiet --python 3.12 --with pytest --with langgraph==1.2.22 pytest -q scripts/tests

## test-projects: lint and test every project with the fake LLM (no API keys needed)
test-projects:
	@for p in $(PROJECTS); do \
		echo "==> $$p"; \
		(cd $$p && uv sync --quiet && uv run ruff check . && uv run pytest -q) || exit 1; \
	done

## links: check every link, including external ones (needs network)
links:
	lychee --config lychee.toml "./**/*.md"

SITE_ENV := NO_MKDOCS_2_WARNING=1 DISABLE_MKDOCS_2_WARNING=true

## site: build the website from the same markdown (strict: fails on broken links)
site:
	$(SITE_ENV) uv run --python 3.12 --with-requirements requirements-site.txt mkdocs build --strict

## site-serve: preview the website at http://127.0.0.1:8000 with live reload
site-serve:
	$(SITE_ENV) uv run --python 3.12 --with-requirements requirements-site.txt mkdocs serve
