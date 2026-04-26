---
title: Contributing
description: How to contribute code, docs, translations, and bug reports to RomM
---

# Contributing

Thanks for considering it. A few ground rules up front, then the mechanics.

<!-- prettier-ignore -->
!!! important "Big changes: open an issue first"
    Planning a large feature or architectural change? Open a GitHub issue **and** drop into the [Discord](https://discord.gg/romm) before coding. A rejected 2,000-line PR is nobody's idea of fun.

The project follows the [Contributor Covenant](https://github.com/rommapp/romm/blob/master/CODE_OF_CONDUCT.md). By contributing, you agree to uphold it.

## AI assistance: please disclose

<!-- prettier-ignore -->
!!! warning "Required disclosure"
    If you use **any kind of AI assistance** to contribute, disclose it in the PR, including the extent of the assistance (docs only vs. full code generation). Trivial tab completion doesn't count, anything more does. If your PR responses are AI-generated, disclose that too.

Examples:

> This PR was written primarily by Claude Code.

> I consulted ChatGPT to understand the codebase but the solution was authored manually.

This isn't gatekeeping AI contributions, it's about calibration: AI-assisted code ranges from "fantastic" to "hallucinated nonsense", and reviewers need to know how much scrutiny to apply. Failing to disclose is rude to the humans reading your PR, so please don't.

## What you can contribute

### Code

- **Bug fixes**: small, focused fixes are welcome without pre-discussion
- **Features**: open an issue first for anything non-trivial
- **Refactors**: open an issue first. Refactors without a clear user-facing win are usually rejected

### Documentation

You're on the docs site right now. If something's wrong, unclear, or missing:

- PRs welcome against [rommapp/docs](https://github.com/rommapp/docs)
- Small fixes (typos, broken links) don't need an issue first
- Bigger changes (restructuring, new sections): open an issue or ping in Discord first

Building docs locally is covered in the docs repo's `CONTRIBUTING.md`. Short version:

```sh
uv venv && source .venv/bin/activate
uv sync --all-extras --dev
uv run mkdocs serve
```

### Translations

Drop a new folder under `frontend/src/locales/` using the existing language files as a template, translate the strings, and open a PR. Partial translations are merged, since an 80%-translated locale is better than nothing. Full workflow in [Translations (i18n)](i18n.md).

### Bug reports

[Open an issue](https://github.com/rommapp/romm/issues) with:

- What happened, what you expected
- Exact reproduction steps
- RomM version and how you deployed it (Docker tag, Unraid, K8s, etc.)
- Relevant logs (`docker logs romm`, redact any secrets)

The bug report template prompts for all of this.

## Pull request mechanics

1. Fork the repository on GitHub.
2. Clone your fork:

    ```sh
    git clone https://github.com/<you>/romm.git
    ```

3. Check out `master`:

    ```sh
    cd romm && git checkout master
    ```

4. Set up your dev environment: [Development Setup](development-setup.md).
5. Create a branch:

    ```sh
    git checkout -b short-feature-name
    ```

6. Make the change, commit with a descriptive message:

    ```sh
    git commit -am "Add support for IGDB alternate-name matching"
    ```

7. Push:

    ```sh
    git push origin short-feature-name
    ```

8. Open a PR against `master` on `rommapp/romm`.

## PR guidelines

- **Lint clean.** `trunk check` must pass or CI will block, see [Development Setup → Linting](development-setup.md#linting) for setup.
- **Tests pass and new behaviour gets new tests.** `uv run pytest` must be green, and any new behaviour needs coverage.
- **Docs updated when behaviour changes.** Even a one-line update beats stale docs sitting around for the next person.
- **Clear title and description.** "Fix bug" isn't a title, but "Fix scan skipping multi-disc PS1 games when first disc is a .chd" is.
- **Tight scope.** One concern per PR. Small drive-by refactors are fine, scorched-earth rewrites aren't.

## Code style

Match the surrounding code. If you use VS Code (or a compatible editor), these extensions match what maintainers run:

- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar)

## Licensing

By contributing, you agree your contributions are licensed under the project's [LICENSE](https://github.com/rommapp/romm/blob/master/LICENSE), which is AGPL-3.0 for the core app.

Thanks for helping make RomM better.
