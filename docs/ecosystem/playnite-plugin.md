---
title: Playnite Plugin
description: Import your RomM library into Playnite on Windows.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Playnite Plugin

<div align="center">
    <img src="../../resources/romm/integrations/playnite.svg" height="200px" width="200px" alt="romm[playnite] logo">
</div>

[Playnite](https://playnite.link) is a unified, open-source game library manager for Windows: one place to launch Steam, Epic, GOG, RetroArch, and emulated games. This plugin imports your RomM library into Playnite, so your RomM ROMs appear alongside your Steam games.

- **Repo:** [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin)
- **Language:** C#
- **License:** GPL-3.0
- **Platforms:** Windows (Playnite)

## What it does

- Queries the RomM API to pull your library metadata
- Creates Playnite library entries for every RomM game
- Downloads a ROM on demand when you click **Install** in Playnite
- Launches via your configured emulator (Playnite's existing emulator config)

## Installing

Four paths, pick whichever's easiest:

- **A.** Paste this URL into a browser to launch Playnite and install automatically:
  `playnite://playnite/installaddon/RomM_9700aa21-447d-41b4-a989-acd38f407d9f`
- **B.** [Playnite add-ons website](https://playnite.link/addons.html#RomM_9700aa21-447d-41b4-a989-acd38f407d9f) → Install
- **C.** From inside Playnite: **Menu → Add-ons → Browse → Libraries**, search `RomM`, Install
- **D.** Download the `.pext` file from [GitHub Releases](https://github.com/rommapp/playnite-plugin/releases/latest) and drop it onto Playnite.

## Setup

### 1. Configure at least one emulator in Playnite

The plugin needs to know how to launch a game. **If no emulators are configured, setup can't finish.**

Playnite: **Menu → Library → Configure Emulators → Add emulator**. Add whatever emulators cover your ROMs (Dolphin, RetroArch, Duckstation, etc.). Built-in presets are fine for most common emulators.

### 2. Configure the plugin

Playnite: **Menu → Library → Configure Integrations → RomM**.

#### Authentication

- **Host URL**: your RomM URL, including scheme, no trailing slash. Examples:
    - ✓ `https://romm.example.com`
    - ✗ `romm.example.com`
    - ✗ `https://romm.example.com/`
- **Username + password**: Playnite stores these in plaintext. Use a **dedicated Viewer-role account** for Playnite, not your admin account.

<!-- prettier-ignore -->
!!! tip "Use a Client API Token instead"
    If your RomM version supports API tokens, create a Viewer-scoped [Client API Token](client-api-tokens.md) and use it instead of a password. Safer and easier to revoke.

#### Emulator path mappings

One mapping per platform:

| Field            | Purpose                           | Example           | Required |
| ---------------- | --------------------------------- | ----------------- | :------: |
| Emulator         | Which Playnite emulator to use    | Dolphin           |    ✓     |
| Emulator Profile | The profile within the emulator   | Nintendo GameCube |    ✓     |
| Platform         | The RomM platform slug            | Nintendo GameCube |    ✓     |
| Destination Path | Where downloaded ROMs are stored  | `C:\roms\gc`      |    ✓     |
| Auto-extract     | Unpack zipped ROMs after download |                   |          |
| Enabled          | Whether this mapping is active    |                   |          |

Map every platform you want Playnite to see. Platforms without a mapping are skipped during import.

## Importing your library

**Menu → Library → Import RomM library.**

Playnite queries RomM, finds every game matching your emulator path mappings, and creates Playnite library entries for each. Covers and metadata pull through.

### Installing a game

Click **Install** on a game card. The plugin:

1. Downloads the ROM from RomM.
2. Writes it to the destination path for that platform.
3. Optionally extracts (default: on).
4. Marks the game installed in Playnite.

**Launch** runs the game with the configured emulator, same as any Playnite-managed emulated game.

### Uninstalling

**Uninstall** in Playnite deletes the local ROM file and marks the game uninstalled. The RomM-side entry is untouched.

## Refreshing

Playnite caches library state. When RomM's library changes, re-run **Import RomM library** to pick up new games.

For automatic refresh: use Playnite's scheduled-library-refresh add-on, or manually re-import periodically.

## Troubleshooting

- **"Unable to connect".** Check the URL scheme, host, and that RomM is reachable from this machine (corporate firewalls, etc.).
- **"Authentication failed".** Username/password mismatch, or the account is disabled. If using a token, make sure it has `roms.read` + `platforms.read`.
- **No games imported.** Emulator path mappings don't cover any platforms in your RomM library. Add mappings for your platforms.
- **Install fails.** Destination path isn't writable, or disk is full.
- **Wrong emulator launches.** Fix the mapping for that platform.

## See also

- [Client API Tokens](client-api-tokens.md): recommended auth method
- [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin): source, issues, releases
- [Playnite docs](https://playnite.link/docs/): Playnite basics if you're new to it
