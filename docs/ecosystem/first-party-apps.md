---
title: First-Party Apps
description: Official clients for Android, Windows, and Linux handhelds.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# First-Party Apps

These are the only clients built and maintained by the team. Pick the one(s) that matches your device(s):

| App                                | Platform                          |
| ---------------------------------- | --------------------------------- |
| [Argosy Launcher](#argosy-launcher) | Android (AYN Thor, Retroid, etc.)   |
| [Grout](#grout)                     | Linux (muOS, MinUI, NextUI, etc.)     |
| [Playnite Plugin](#playnite-plugin) | Windows ([Playnite](https://playnite.link)) |

For third-party clients, see the [Community section in the README](https://github.com/rommapp/romm/#community).

## Argosy Launcher

**Argosy Launcher** is our first-party Android app: browse your library, download ROMs on the fly, and launch into RetroArch or your emulator of choice.

- **Repo:** [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher)
- **Language:** Kotlin
- **License:** GPL-3.0
- **Platforms:** Android

### What it does

- Browses your full library from an Android device
- Handles authentication via [Client API Tokens](client-api-tokens.md), paired over a short code so you don't type a 44-character string
- Downloads ROMs on demand to your device's storage
- Launches RetroArch (or another configured emulator) with the downloaded ROM
- Syncs saves / states back to RomM when you finish a session (optional)

## Grout

**Grout** is our first-party companion for Linux-based handhelds, specifically [muOS](https://muos.dev) and [NextUI](https://github.com/mattsays/nextui). Syncs ROMs, saves, and states bidirectionally with your instance over Wi-Fi.

- **Repo:** [rommapp/grout](https://github.com/rommapp/grout)
- **Language:** Go
- **License:** MIT
- **Platforms:** muOS (Anbernic and similar ARM handhelds), NextUI

### What it does

- Connects to your instance using a [Client API Token](client-api-tokens.md)
- **Pulls** ROMs from your instance to the handheld's SD card, organised into muOS / NextUI's expected folder layout
- **Pushes** saves and states back to your instance when you finish a session
- **Schedules** sync runs: on idle, on session end, or on a cron
- Works fully offline between syncs, so the handheld doesn't need your instance to play

## Playnite Plugin

<div align="center">
    <img src="../../resources/romm/integrations/playnite.svg" height="200px" width="200px" alt="romm[playnite] logo">
</div>

[Playnite](https://playnite.link) is a unified, open-source game library manager for Windows: one place to launch Steam, Epic, GOG, RetroArch, and emulated games. This plugin imports your library into Playnite, so your ROMs appear alongside your Steam games.

- **Repo:** [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin)
- **Language:** C#
- **License:** GPL-3.0
- **Platforms:** Windows (Playnite)

### What it does

- Queries the API to pull your library metadata
- Creates Playnite library entries for every game
- Downloads a ROM on demand when you click **Install** in Playnite
- Launches via your configured emulator (using Playnite's existing emulator config)

## See also

- [Client API Tokens](client-api-tokens.md): the auth + pairing flow some of these clients use
- [Community section in the README](https://github.com/rommapp/romm/#community): third-party clients
