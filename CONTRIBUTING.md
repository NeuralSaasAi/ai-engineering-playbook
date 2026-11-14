# Contributing

Thanks for helping. This playbook only works if it stays accurate and easy to understand, so every fix counts, including a single clearer sentence.

## Ways to help

- **Fix something wrong or unclear:** use the [content fix](https://github.com/NeuralSaasAi/ai-engineering-playbook/issues/new?template=content-fix.yml) form, or open a pull request.
- **Report a broken link:** use the [broken link](https://github.com/NeuralSaasAi/ai-engineering-playbook/issues/new?template=broken-link.yml) form.
- **Suggest a topic:** use the [topic request](https://github.com/NeuralSaasAi/ai-engineering-playbook/issues/new?template=topic-request.yml) form.
- **Write a note:** copy [templates/note-template.md](templates/note-template.md) into the right module folder and follow [STYLE.md](STYLE.md).
- **Improve a project:** fixes, clearer READMEs, and tests are welcome. Keep the fake-LLM tests working so nobody needs an API key to run them.

New to pull requests? Click the pencil icon on any page on GitHub, make your edit, and GitHub walks you through the rest.

## What we accept

- Original writing. Don't copy from courses, books, videos or other sites.
- Explanations aimed at beginners to intermediates. Advanced material belongs in "Go deeper" links.
- Sources that are official, primary, or reputable. See [STYLE.md](STYLE.md#sources).
- No promotional links, referral codes or tracking parameters.

## Run the checks locally

You need Python 3.12+, [uv](https://docs.astral.sh/uv/), and Node.js (for the markdown linter).

```bash
make check   # note format, glossary, relative links, markdown lint, all project tests
make links   # external link check (needs lychee: brew install lychee)
```

Run one project's tests:

```bash
cd projects/p2-secure-rag
uv sync
uv run pytest
```

## Disclosure

If you work for, own, or are paid by a product you're adding or editing, say so in the pull request. You're welcome to contribute; we just need to know.

## Code of Conduct

By taking part, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
