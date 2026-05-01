---
title: Ruffle
description: Play Flash and Shockwave games in the browser via the bundled Ruffle player
---

# Ruffle

[Ruffle](https://ruffle.rs/) is a Flash / Shockwave player built with WebAssembly and bundled with the full container image.

<!-- prettier-ignore -->
!!! important "Ruffle needs the right platform folder"
    Ruffle only plays games from platform folders named `flash` or `browser`. If your Flash games are elsewhere, either rename the folder or add a [platform binding](../../reference/configuration-file.md#systemplatforms) in `config.yml`.

No controller mapping, so gamepad-only users will struggle with most Flash titles.

## Supported games

Most 2D Flash games work, but 3D Shockwave and some advanced ActionScript titles may have rendering glitches. See [Ruffle compatibility](https://ruffle.rs/#compatibility) for per-title status.

## Metadata

If you enable the [Flashpoint](../../administration/metadata-providers.md#flashpoint) provider, Ruffle games pick up descriptions, cover art, and tags from the Flashpoint database.

More troubleshooting in [In-Browser Play Troubleshooting](../../troubleshooting/in-browser-play.md).
