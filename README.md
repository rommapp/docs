<div align="center">

  <img src=".github/resources/isotipo.png" height="180px" width="auto" alt="RomM docs logo">
    <h3 style="font-size: 25px;">
    Beautiful, powerful, documentation for RomM
  </h3>

  <br />

[![license-badge-img]][license-badge]
[![discord-badge-img]][discord-badge]

  </div>
</div>

# Overview

This is the official documentation for [RomM](https://romm.app/), the beautiful, powerful self-hosted ROM manager and player. Here you'll find everything you need to know about setting up, configuring, and using RomM.

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

## Contributing

We welcome all types of contributions, from simple typo fixes to new content. If you'd like to contribute, please read our [code of conduct](CODE_OF_CONDUCT.md).

### Setting up the linter

We use [Trunk](https://trunk.io) for linting, which combines multiple linters with sensible defaults and a single configuration file. You'll need to install the Trunk CLI to use it.

#### - Install the Trunk CLI

```sh
curl https://get.trunk.io -fsSL | bash
```

Alternative installation methods can be found [here](https://docs.trunk.io/check/usage#install-the-cli). On commit, the linter will run automatically. To run it manually, use the following commands:

```sh
trunk fmt
trunk check
```

## Deploy

We use [mike]() to build and deploy documentation versions. Manually deploy a version needs to update and push the specific version (or a new one if creating a new version) with the following command:

```sh
uv run mike deploy --push <version> [alias]
```

This will update the `gh-pages` branch and automatically deploys the version with the fix/update to https://docs.romm.app

## Social

Join us on Discord, where you can ask questions, submit ideas, get help, showcase your collection, and discuss RomM with other users.

[![discord-invite]][discord-invite-url]

<!-- Badges -->

[license-badge-img]: https://img.shields.io/github/license/rommapp/wiki?style=for-the-badge&color=a32d2a
[license-badge]: LICENSE
[discord-badge-img]: https://img.shields.io/badge/discord-7289da?style=for-the-badge
[discord-badge]: https://discord.gg/P5HtHnhUDH

<!-- Links -->

[discord-invite]: https://invidget.switchblade.xyz/P5HtHnhUDH
[discord-invite-url]: https://discord.gg/P5HtHnhUDH
