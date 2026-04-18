---
title: Ruffle Configuration
description: Operator-level setup for the Ruffle Flash / Shockwave player.
---

# Ruffle Configuration

[Ruffle](https://ruffle.rs/) is RomM's Flash / Shockwave emulator. End-user details in [In-Browser Play → Ruffle](../using/in-browser-play.md#ruffle). This page is for operators.

## Enable / disable

```yaml
environment:
  - ENABLE_RUFFLE=true     # default
```

Set `false` to hide the Ruffle Play button globally. Useful on the slim image (Ruffle isn't bundled) or when you have no Flash content.

## Platform folder names

Ruffle **only** plays games from platform folders named `flash` or `browser`. No exceptions in 5.0.

If your Flash games live under a differently-named folder:

### Option 1: rename

Just rename the folder to `flash/` and rescan.

### Option 2: remap via `config.yml`

```yaml
system:
  platforms:
    web-games: "flash"    # your-folder: canonical-slug
```

Now `web-games/` is treated as the `flash` platform. See [Configuration File → `system.platforms`](../reference/configuration-file.md#systemplatforms).

## Supported content

- **Flash (SWF):** 2D games, most work cleanly. AS1/AS2 excellent; AS3 still maturing in Ruffle.
- **Shockwave (DCR):** partial support; complex 3D Shockwave games often fail.
- **FLV / F4V:** Flash video; playable but not game-like.

[Ruffle compatibility database](https://ruffle.rs/#compatibility) has per-title status if you want to check a specific game.

## File naming

Ruffle honours the usual [RomM naming conventions](../getting-started/folder-structure.md#naming-convention): filename tags, regions, revisions.

No specific requirements beyond that; Ruffle reads the SWF directly.

## Saves

Flash's "shared objects" (`.sol` files, the Flash equivalent of cookies + saves) are persisted to `/romm/assets/<user>/<rom>/saves/`. Per-user per-ROM. Appears on the game detail's **Game Data** tab like emulator saves.

## Metadata

Metadata coverage for Flash games comes from the [Flashpoint](../administration/metadata-providers.md#flashpoint) provider. Enable:

```yaml
environment:
  - FLASHPOINT_API_ENABLED=true
```

Then run an **Unmatched** scan on your `flash` platform. Titles, descriptions, cover art, tags: all populated if the game exists in Flashpoint's ~180,000-entry database.

## Controls

Flash was designed around mouse + keyboard. Ruffle passes input through natively:

- **Mouse:** full support.
- **Keyboard:** full support.
- **Gamepad: not supported.** Flash games using XInput or similar don't work.

On a handheld / Console Mode, Flash games are generally unplayable unless you've got a touchscreen + keyboard or a mouse.

## Version / updates

Ruffle is bundled in the full RomM image. Updates to Ruffle land when RomM updates its image; there's no separate Ruffle update knob.

## Not in 5.0 yet

- **Per-game config overrides.** Ruffle supports some game-specific options upstream, but RomM doesn't surface them yet.
- **Networking.** Flash games that hit remote servers typically fail (those servers are dead). No proxy / emulated backend for networked Flash games.
- **Control remapping.** Straight passthrough only.

## Troubleshooting

- **Play button is missing on a Flash game.** Platform folder isn't named `flash` or `browser` (or mapped via `system.platforms`).
- **Game loads but blank.** AS3 game Ruffle doesn't handle yet. Check [Ruffle compatibility](https://ruffle.rs/#compatibility).
- **Game says "Ruffle not loaded".** You're on the slim image. Switch to full, or set `ENABLE_RUFFLE=false` to hide the Play button cleanly.

See [In-Browser Play Troubleshooting → Ruffle](../troubleshooting/in-browser-play.md#ruffle-games).

## See also

- [In-Browser Play → Ruffle](../using/in-browser-play.md#ruffle): end-user side.
- [Metadata Providers → Flashpoint](../administration/metadata-providers.md#flashpoint): where Flash metadata comes from.
