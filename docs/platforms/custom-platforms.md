---
title: Custom Platforms
description: Add custom unsupported platforms
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

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

If your platform is one RomM supports but under a different slug, you don't need a custom platform. Just **remap** it in your `config.yml`:

```yaml
system:
    platforms:
        super_nintendo: "snes" # your folder → canonical slug
        psx: "ps"
        game-cube: "ngc"
```

This gets you full metadata provider support with your preferred folder name (see [Configuration File → `system.platforms`](../reference/configuration-file.md#systemplatforms)).

## Adding a custom platform icon

If your platform isn't in [the built-in icons list](https://github.com/rommapp/romm/tree/master/frontend/assets/platforms), RomM shows a default fallback icon.

To load your own:

1. Mount the platform icons directory

Bind-mount a host directory onto the container's icon path:

```yaml
services:
    romm:
        volumes:
            - /path/to/your/icons:/var/www/html/assets/platforms
```

2. Seed it with the official icons

The built-in icons live at [`frontend/assets/platforms`](https://github.com/rommapp/romm/tree/master/frontend/assets/platforms). Download them all and drop into your mounted directory, otherwise built-in platforms lose their icons too (because your mount overrides the whole directory).

3. Add your custom `.ico` files

The filename has to **match the platform slug**. Examples:

| Platform            | Platform slug                  | Filename                  |
| ------------------- | ------------------------------ | ------------------------- |
| Amstrad CPC         | `acpc`                         | `acpc.ico`                |
| My Homebrew Console | `my-homebrew-console` (custom) | `my-homebrew-console.ico` |
| NES                 | `nes`                          | `nes.ico`                 |

4. Restart RomM

`docker compose up -d` picks up the new icon mount.

To replace an existing platform's icon, use a filename matching an existing platform's slug and your file overrides the built-in.

## Screenshot

<img width="2459" alt="Platforms view with custom icons" src="https://github.com/rommapp/romm/assets/3247106/1831c206-b431-41c2-9761-49c132f40ee0">
