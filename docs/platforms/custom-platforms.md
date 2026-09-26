---
title: Custom Platforms
description: Add custom unsupported platforms
---

# Custom Platforms

RomM ships with support for ~400 platforms. If yours isn't in [the list](supported-platforms.md), you can still load it as a custom platform, but we won't have metadata provider coverage for it.

## Adding a custom platform

Make a folder for the platform under your library root. Rules:

- **All lowercase.**
- **Use `-` to separate words.**
- **No whitespace.**

Examples:

| Folder name           | Displays as         |
| --------------------- | ------------------- |
| `pocket-challenge-v2` | Pocket Challenge V2 |
| `my-homebrew-console` | My Homebrew Console |
| `wasm4`               | Wasm4               |

Then either run a **Quick Scan** (the platform is auto-discovered) or trigger a **New Platforms** scan from the **Scan** page.

## Mapping to a canonical platform (preferred when possible)

If your platform is one RomM supports but your folder is named differently, you don't need a custom platform.

Check the [folder name aliases](supported-platforms.md#folder-name-aliases) first: the names Batocera, RetroBat and ES-DE use (`megadrive/`, `gamecube/`, `n3ds/`, and ~140 more) already resolve on their own. For anything else, **remap** it in your `config.yml`:

```yaml
system:
    platforms:
        super_nintendo: "snes" # your folder → canonical slug
        game-cube: "ngc"
```

This gets you full metadata provider support with your preferred folder name (see [Configuration File → `system.platforms`](../reference/configuration-file.md#systemplatforms)).
