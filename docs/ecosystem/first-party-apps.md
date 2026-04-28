---
title: First-Party Apps
description: Official RomM clients — Argosy Launcher (Android), Grout (Linux handhelds), and the Playnite Plugin (Windows).
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# First-Party Apps

These are the clients the RomM team builds and supports directly. Pick the one that matches your device:

| App                                | Platform                          | Use it for                                                  |
| ---------------------------------- | --------------------------------- | ----------------------------------------------------------- |
| [Argosy Launcher](#argosy-launcher) | Android (phones, Retroid, etc.)   | Browse, download, launch into native emulators              |
| [Grout](#grout)                     | muOS / NextUI Linux handhelds     | Bidirectional ROM, save, and state sync                     |
| [Playnite Plugin](#playnite-plugin) | Windows ([Playnite](https://playnite.link)) | Imports your RomM library next to Steam, Epic, GOG, etc. |

For third-party clients, see the [Community section in the RomM README](https://github.com/rommapp/romm/#community).

## Argosy Launcher

**Argosy Launcher** is RomM's first-party Android app: browse your library, download ROMs on the fly, and launch into RetroArch or your emulator of choice.

- **Repo:** [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher)
- **Language:** Kotlin
- **License:** GPL-3.0
- **Platforms:** Android

### What it does

- Browses your full RomM library from an Android device
- Handles authentication via [Client API Tokens](client-api-tokens.md), paired over a short code so you don't type a 44-character string
- Downloads ROMs on demand to your device's storage
- Launches RetroArch (or another configured emulator) with the downloaded ROM
- Syncs saves / states back to RomM when you finish a session (optional)

### Installing

#### From a release

1. Grab the latest `.apk` from [GitHub Releases](https://github.com/rommapp/argosy-launcher/releases/latest).
2. Install via your Android device's package installer (you may need to enable "Install from unknown sources" in Settings).

#### Via F-Droid / Play Store

Not currently on either, so APK sideloading is the path for now.

### First-time setup

1. Launch Argosy.
2. Enter your RomM URL (e.g. `https://demo.romm.app`), which needs HTTPS in production.
3. Choose **Pair Device**.
4. Argosy shows a pairing URL or QR code: open it on a device that's already signed into RomM.
5. Enter the 8-digit code Argosy displayed on that RomM page.
6. Accept, and Argosy receives a Client API Token bound to your RomM account.

From here, Argosy lists your library. Full pairing-flow details in [Client API Tokens](client-api-tokens.md).

### Using Argosy

#### Browse

The main view mirrors RomM's platform-and-collection layout: tap a platform to see its games, and search works the same as the RomM web UI.

#### Download and launch

Tap a game → **Download** and Argosy pulls the ROM to device storage. Once downloaded, **Play** launches it with your configured emulator.

#### Emulator configuration

Argosy → Settings → Emulators. For each platform:

- Pick the external emulator app (RetroArch, Duckstation, PPSSPP, etc.).
- Optionally pass core-specific args.

RetroArch users: Argosy can auto-detect installed RetroArch cores and map platforms to them.

#### Save sync

Argosy → Settings → Sync. Two modes:

- **On session end**: uploads saves back to RomM when you exit the emulator
- **Manual**: you tap Upload when you want.

Saves show up in RomM's **Game Data** tab on the game, same as in-browser saves: see [Saves & States](../using/saves-and-states.md).

### Permissions

Argosy needs:

- **Storage**: to save downloaded ROMs
- **Network**: to talk to your RomM instance
- **Optional: Notifications**: download-complete and sync-complete pings

No other permissions: the app doesn't request contacts, camera, location, or anything else.

### Troubleshooting

- **Can't connect to RomM**: check the URL (including `https://`) and that the RomM instance is reachable from your mobile network. Cellular might be blocked, so try Wi-Fi first.
- **Token invalid**: pair again, since tokens can expire or be revoked on the RomM side.
- **Emulator won't launch**: make sure the emulator app is installed and Argosy has permission to open it, as some emulators require an intent-filter setup.
- **Downloads fail partway**: usually network, and Argosy resumes on retry.

Full sync-specific debugging in [Device Sync Troubleshooting](../troubleshooting/sync.md).

## Grout

**Grout** is RomM's first-party companion for Linux-based handhelds, specifically [muOS](https://muos.dev) and [NextUI](https://github.com/mattsays/nextui). Syncs ROMs, saves, and states bidirectionally with your RomM instance over Wi-Fi.

- **Repo:** [rommapp/grout](https://github.com/rommapp/grout)
- **Language:** Go
- **License:** MIT
- **Platforms:** muOS (Anbernic and similar ARM handhelds), NextUI

### What it does

- Connects to your RomM instance using a [Client API Token](client-api-tokens.md)
- **Pulls** ROMs from RomM to the handheld's SD card, organised into muOS / NextUI's expected folder layout
- **Pushes** saves and states back to RomM when you finish a session
- **Schedules** sync runs: on idle, on session end, or on a cron
- Works fully offline between syncs, so the handheld doesn't need RomM to play

### Why Grout (and not Argosy)?

- [Argosy](#argosy-launcher) is Android-native. Good for Android handhelds (Retroid Pocket running Android, phones)
- Grout is for non-Android Linux handhelds. muOS and NextUI are Linux, not Android. Argosy's APK won't install.

Same underlying protocol but different client for different OS.

### Installing

#### On muOS

1. Grab the latest `.muxapp` release from [GitHub Releases](https://github.com/rommapp/grout/releases/latest).
2. Copy to `/mnt/mmc/ARCHIVE/` on the device (USB, SD swap, or SSH).
3. Launch **Archive Manager** from the Applications menu.
4. Select the Grout `.muxapp` → install.
5. After install, find **Grout** under Applications.

#### On NextUI

1. Download the NextUI-flavoured release from the same releases page.
2. Follow NextUI's standard app install flow (paths differ by device, see NextUI docs).

### First-time setup

1. Launch Grout on the handheld.
2. Enter your RomM URL.
3. **Pair Device**: Grout displays an 8-digit code.
4. On any device already signed into RomM, navigate to **Profile → Client API Tokens → + New Token** → create a new token → **Pair Device** → enter the code shown on Grout.
5. Grout receives the token, confirms pairing, and fetches your library metadata.

Details on the pairing flow in [Client API Tokens](client-api-tokens.md).

### Using Grout

#### Browse

Grout's main view lists platforms. Select one to see available ROMs. Metadata (titles, cover art) is pulled live from RomM.

#### Download ROMs

Select a ROM → **Download**. Grout pulls the file to the expected location on the SD card, so muOS / NextUI's native launcher sees it on next refresh.

Bulk select for multi-file downloads, useful for pulling a whole collection at once.

#### Sync cadence

Grout → Settings → Sync:

- **Pull** cadence: how often to check RomM for new ROMs (default: manual, and can be set to every N minutes when on Wi-Fi)
- **Push** cadence: how often to upload saves (default: on session end)
- **Full sync**: manual. Triggers a full bidirectional sync right now

#### What pushes back to RomM

- **Save files.** Once a session ends, Grout uploads any changed saves to RomM.
- **Save states.** Same, if enabled in settings
- **Play session records.** Start/end times for the **Continue Playing** ribbon and per-ROM playtime on RomM

### Permissions and access

Grout uses your Client API Token for all API calls. Token scopes:

- `roms.read`, `platforms.read`, `collections.read`: to browse
- `assets.read`, `assets.write`: to sync saves
- `devices.read`, `devices.write`: to register as a device
- `firmware.read`: if you're syncing firmware too

Scope the token narrowly when creating: default scopes are fine for most users but an admin shouldn't hand Grout `users.write` just because the token-creation page offers it.

### SSH sync (operator-side)

If you want Grout to pull from RomM over SSH rather than HTTPS (e.g. on a trusted LAN with no reverse proxy) see [SSH Sync](ssh-sync.md) for the server-side config. Grout supports both modes, selectable in Settings → Connection.

### Troubleshooting

- **Can't see the handheld's Wi-Fi on RomM's network.** Make sure both are on the same SSID / VLAN.
- **Token invalid.** Re-pair, because the token was revoked or expired.
- **Saves aren't syncing.** Check the sync cadence is set to something other than "never", and that the handheld actually has network during the sync window.
- **"Device not registered".** The pairing step wasn't completed. Re-run pairing from scratch.

More in [Device Sync Troubleshooting](../troubleshooting/sync.md).

## Playnite Plugin

<div align="center">
    <img src="../../resources/romm/integrations/playnite.svg" height="200px" width="200px" alt="romm[playnite] logo">
</div>

[Playnite](https://playnite.link) is a unified, open-source game library manager for Windows: one place to launch Steam, Epic, GOG, RetroArch, and emulated games. This plugin imports your RomM library into Playnite, so your RomM ROMs appear alongside your Steam games.

- **Repo:** [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin)
- **Language:** C#
- **License:** GPL-3.0
- **Platforms:** Windows (Playnite)

### What it does

- Queries the RomM API to pull your library metadata
- Creates Playnite library entries for every RomM game
- Downloads a ROM on demand when you click **Install** in Playnite
- Launches via your configured emulator (Playnite's existing emulator config)

### Installing

Four paths, pick whichever's easiest:

- **A.** Paste this URL into a browser to launch Playnite and install automatically:
  `playnite://playnite/installaddon/RomM_9700aa21-447d-41b4-a989-acd38f407d9f`
- **B.** [Playnite add-ons website](https://playnite.link/addons.html#RomM_9700aa21-447d-41b4-a989-acd38f407d9f) → Install
- **C.** From inside Playnite: **Menu → Add-ons → Browse → Libraries**, search `RomM`, Install
- **D.** Download the `.pext` file from [GitHub Releases](https://github.com/rommapp/playnite-plugin/releases/latest) and drop it onto Playnite.

### Setup

1. Configure at least one emulator in Playnite

The plugin needs to know how to launch a game. **If no emulators are configured, setup can't finish.**

Playnite: **Menu → Library → Configure Emulators → Add emulator**. Add whatever emulators cover your ROMs (Dolphin, RetroArch, Duckstation, etc.). Built-in presets are fine for most common emulators.

2. Configure the plugin

Playnite: **Menu → Library → Configure Integrations → RomM**.

#### Authentication

- **Host URL**: your RomM URL, including scheme, no trailing slash. Examples:
    - ✓ `https://demo.romm.app`
    - ✗ `demo.romm.app`
    - ✗ `https://demo.romm.app/`
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

### Importing your library

**Menu → Library → Import RomM library.**

Playnite queries RomM, finds every game matching your emulator path mappings, and creates Playnite library entries for each. Covers and metadata pull through.

#### Installing a game

Click **Install** on a game card. The plugin:

1. Downloads the ROM from RomM.
2. Writes it to the destination path for that platform.
3. Optionally extracts (default: on).
4. Marks the game installed in Playnite.

**Launch** runs the game with the configured emulator, same as any Playnite-managed emulated game.

#### Uninstalling

**Uninstall** in Playnite deletes the local ROM file and marks the game uninstalled. The RomM-side entry is untouched.

### Refreshing

Playnite caches library state. When RomM's library changes, re-run **Import RomM library** to pick up new games.

For automatic refresh: use Playnite's scheduled-library-refresh add-on, or manually re-import periodically.

### Troubleshooting

- **"Unable to connect".** Check the URL scheme, host, and that RomM is reachable from this machine (corporate firewalls, etc.).
- **"Authentication failed".** Username/password mismatch, or the account is disabled. If using a token, make sure it has `roms.read` + `platforms.read`.
- **No games imported.** Emulator path mappings don't cover any platforms in your RomM library. Add mappings for your platforms.
- **Install fails.** Destination path isn't writable, or disk is full.
- **Wrong emulator launches.** Fix the mapping for that platform.

## See also

- [Client API Tokens](client-api-tokens.md): the auth + pairing flow these clients use
- [Device Sync Protocol](../developers/device-sync-protocol.md): wire-level sync protocol
- [SSH Sync](ssh-sync.md): operator-side SSH config for Grout
- [Community section in the RomM README](https://github.com/rommapp/romm/#community): third-party clients
