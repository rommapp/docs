---
title: First-Party Apps
description: Official clients for Android, Windows, and Linux handhelds.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->
<!-- trunk-ignore-all(markdownlint/MD024) -->

# First-Party Apps

The team builds and maintains only these clients. Pick the ones that match your devices:

| App                                 | Platform                                    |
| ----------------------------------- | ------------------------------------------- |
| [Argosy Launcher](#argosy-launcher) | Android (AYN Thor, Retroid, etc.)           |
| [Grout](#grout)                     | Linux (muOS, MinUI, NextUI, etc.)           |
| [Playnite Plugin](#playnite-plugin) | Windows ([Playnite](https://playnite.link)) |

For third-party clients, see the [Community section in the README](https://github.com/rommapp/romm/#community). To compare features across all of these apps, including which systems each one syncs saves for, see the [App Feature Comparison](app-comparison.md).

## Argosy Launcher

**Argosy Launcher** is our first-party Android app: browse your library, download ROMs on the fly, and launch into RetroArch or your emulator of choice.

<div align="center">
    <img src="../../resources/romm/apps/argosy.png" alt="Argosy Launcher screenshot" style="max-width: 600px; width: 100%;">
</div>

- **Repo:** [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher)
- **Language:** Kotlin
- **License:** GPL-3.0
- **Platforms:** Android

### What it does

- Browses your full library from an Android device
- Handles authentication via [Client API Tokens](../developers/client-api-tokens.md), paired over a short code so you don't type a 68-character string
- Downloads ROMs on demand to your device's storage
- Launches RetroArch (or another configured emulator) with the downloaded ROM
- Syncs saves/states back to RomM when you finish a session (optional); see [which emulators it covers](app-comparison.md#argosy)

### Setup

See [Getting Started](https://github.com/rommapp/argosy-launcher#getting-started) in the Argosy repo for install and pairing instructions.

## Grout

**Grout** is our first-party companion for Linux-based handhelds, specifically [muOS](https://muos.dev) and [NextUI](https://github.com/mattsays/nextui). It downloads ROMs, box art and BIOS files from your instance and syncs saves both ways over Wi-Fi.

<div align="center">
    <img src="../../resources/romm/apps/grout.png" alt="Grout screenshot" style="max-width: 600px; width: 100%;">
</div>

- **Repo:** [rommapp/grout](https://github.com/rommapp/grout)
- **Language:** Go
- **License:** MIT
- **Platforms:** muOS (Anbernic and similar ARM handhelds), NextUI

### What it does

- Connects to your instance using a [Client API Token](../developers/client-api-tokens.md)
- Pulls ROMs from your instance to the handheld's SD card, organised into muOS/NextUI's expected folder layout
- Syncs saves both ways when you run **Sync Now**; save states don't sync, and coverage [varies by firmware](app-comparison.md#grout)
- Works fully offline between syncs so the handheld doesn't need your instance to play

### Setup

See [Getting Started](https://grout.romm.app/getting-started/) in the Grout docs for install and sync configuration instructions.

## Playnite Plugin

<div align="center">
    <img src="../../resources/romm/integrations/playnite.svg" height="200px" width="200px" alt="romm[playnite] logo">
</div>

[Playnite](https://playnite.link) is a unified, open-source game library manager for Windows: one place to launch Steam, Epic, GOG, RetroArch, and emulated games. This plugin imports your library into Playnite, so your ROMs appear alongside your Steam games.

<div align="center">
    <img src="../../resources/romm/apps/playnite.png" alt="Playnite Plugin screenshot" style="max-width: 600px; width: 100%;">
</div>

- **Repo:** [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin)
- **Language:** C#
- **License:** GPL-3.0
- **Platforms:** Windows (Playnite)

### What it does

- Queries the API to pull your library metadata
- Creates Playnite library entries for every game
- Downloads a ROM on demand when you click **Install** in Playnite
- Launches via your configured emulator (using Playnite's existing emulator config)
- Syncs RetroArch saves with RomM before launch and after you quit (opt-in; see [save sync](app-comparison.md#playnite-plugin))

### Setup

#### Install the plugin

Install through any of these methods:

- **Direct launch:** open `playnite://playnite/installaddon/RomM_9700aa21-447d-41b4-a989-acd38f407d9f` in your browser
- **In-app:** go to **Menu → Add-ons → Browse → Libraries**, search for **RomM**, and select **Install**
- **Add-ons website:** download it from the [Playnite add-ons portal](https://playnite.link/addons.html)
- **Manual:** download the `.pext` file from the [releases page](https://github.com/rommapp/playnite-plugin/releases) and drag it onto Playnite

#### Configure an emulator

You need at least one emulator installed and configured in Playnite before the plugin can launch anything, so add one under **Menu → Library → Configure Emulators → Add emulator** if you haven't already.

#### Connect to your instance

Open **Menu → Library → Configure Integrations → RomM** and enter:

- **Host URL**, including the protocol and without a trailing slash, for example `https://romm.example.com`
- Your **username** and **password**

Passwords are stored in plaintext in Playnite, so use a separate account with a read-only permission group rather than your main credentials.

#### Map emulator paths

For each platform you want to import, add a mapping with these fields:

- **Emulator:** a built-in or custom emulator
- **Emulator Profile:** the matching profile for that emulator
- **Platform:** the console or platform to map
- **Destination Path:** where downloaded ROMs are stored, for example `C:\roms\gc`
- **Auto-extract:** whether to automatically extract compressed files

#### Import your library

Select **Menu → Library → Import RomM library**. Every game matching your emulator path mappings is imported into Playnite, downloaded to its destination path on demand, and launched through the configured emulator.

## See also

- [Client API Tokens](../developers/client-api-tokens.md): the auth + pairing flow some of these clients use
- [Community section in the README](https://github.com/rommapp/romm/#community): third-party clients
