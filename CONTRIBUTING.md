# Contributing to RomM's documentation

Thank you for considering contributing to RomM's documentation! This document outlines some guidelines to help you get started with your contributions.

**If you're looking to implement a large feature or make significant changes to the project, it's best to open an issue first AND join the Discord to discuss your ideas with the maintainers.**

## Code of Conduct

Please note that this project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating in this project, you are expected to uphold this code.

## Setting up the linter

We use [Trunk](https://trunk.io) for linting, which combines multiple linters with sensible defaults and a single configuration file. You'll need to install the Trunk CLI to use it.

### - Install the Trunk CLI

```sh
curl https://get.trunk.io -fsSL | bash
```

Alternative installation methods can be found [here](https://docs.trunk.io/check/usage#install-the-cli). On commit, the linter will run automatically. To run it manually, use the following commands:

```sh
trunk fmt
trunk check
```

## Building the documentation

We use `uv` to build the documentation. To install it, run:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

And activate it:

```sh
uv venv
source .venv/bin/activate
```

Then install python and the required dependencies:

```sh
uv python install
uv sync --all-extras --dev
```

Finally run the following command to serve the documentation from a local server:

```sh
uv run mkdocs serve [-a ip:port] --livereload
```

## Deploy

We use [mike](https://github.com/jimporter/mike) to build and deploy documentation versions. Manually deploy a version needs to update and push the specific version (or a new one if creating a new version) with the following command:

```sh
uv run mike deploy --push --update-aliases <version> [alias]
```

This will update the `gh-pages` branch and automatically deploys the version with the fix/update to <https://docs.romm.app>.

## Pull Request Guidelines

- Make sure your code follows the project's coding standards.
- Test your changes locally before opening a pull request.
- Update the documentation if necessary.
- Ensure all existing tests pass, and add new tests for new functionality.
- Use clear and descriptive titles and descriptions for your pull requests.

## Issue Reporting

If you encounter any bugs or have suggestions for improvements, please [create an issue](https://github.com/rommapp/docs/issues) on GitHub. Provide as much detail as possible, including steps to reproduce the issue if applicable.

## Licensing

By contributing to RomM's documentation, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE).

---

Thank you for contributing to RomM's documentation! Your help is greatly appreciated.