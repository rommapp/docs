---
title: Custom Platforms
description: Add platforms RomM doesn't natively support, plus custom platform icons.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Custom Platforms

RomM ships with support for ~400 platforms. If yours isn't in [the list](supported-platforms.md), you can still load it as a custom platform. RomM just won't have metadata-provider coverage for it.

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

If your platform is one RomM supports but under a different slug, you don't need a custom platform. Just **remap**. Add to `config.yml`:

```yaml
system:
    platforms:
        super_nintendo: "snes" # your folder → canonical slug
        psx: "ps"
        game-cube: "ngc"
```

This gets you full metadata-provider support with your preferred folder name. See [Configuration File → `system.platforms`](../reference/configuration-file.md#systemplatforms).

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

RomM's built-in icons live at [`frontend/assets/platforms`](https://github.com/rommapp/romm/tree/master/frontend/assets/platforms). Download them all and drop into your mounted directory, otherwise built-in platforms lose their icons too (because your mount overrides the whole directory).

3. Add your custom `.ico` files

The filename has to **match the IGDB platform slug**. Examples:

| Platform            | IGDB slug                      | Filename                  |
| ------------------- | ------------------------------ | ------------------------- |
| Amstrad CPC         | `acpc`                         | `acpc.ico`                |
| Pocket Challenge V2 | `pocket-challenge-v2` (custom) | `pocket-challenge-v2.ico` |
| NES                 | `nes`                          | `nes.ico`                 |

Find the slug in the URL of the platform's IGDB page, e.g. [igdb.com/platforms/acpc](https://www.igdb.com/platforms/acpc) → slug is `acpc`.

4. Restart RomM

`docker compose up -d` picks up the new icon mount.

### Replacing an existing platform's icon

Same mechanic: just use a filename matching an existing platform's slug and your file overrides the built-in.

## What custom platforms don't get

- **Metadata provider coverage.** Providers are IGDB-slug-driven. A genuinely unknown platform won't have IGDB / ScreenScraper / MobyGames data.
- **EmulatorJS support.** The platform has to match a known EmulatorJS core. See [Supported Platforms → EmulatorJS column](supported-platforms.md).
- **RetroAchievements.** Hash-based but restricted to RA-supported platforms

For the niche platform case, you'll likely rely on filename-only matching (no provider) and browsing the library like a straight file system.

## Contributing a platform

If you've added a custom platform that should be supported natively by RomM (e.g. a widely-used platform that's missing) open an issue on [rommapp/romm](https://github.com/rommapp/romm/issues) with:

- Platform name
- IGDB platform URL (if it exists on IGDB)
- Typical file extensions
- Suggested canonical slug

The team adds platforms fairly aggressively if they see community demand.

## Screenshot

<img width="2459" alt="Platforms view with custom icons" src="https://github.com/rommapp/romm/assets/3247106/1831c206-b431-41c2-9761-49c132f40ee0">
