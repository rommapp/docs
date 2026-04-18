---
title: Grout
description: Official Linux handheld companion for muOS and NextUI, sync ROMs and saves from RomM.
---

# Grout

**Grout** is RomM's first-party companion for Linux-based handhelds, specifically [muOS](https://muos.dev) and [NextUI](https://github.com/mattsays/nextui). Syncs ROMs, saves, and states bidirectionally with your RomM instance over Wi-Fi.

- **Repo:** [rommapp/grout](https://github.com/rommapp/grout)
- **Language:** Go
- **License:** MIT
- **Platforms:** muOS (Anbernic and similar ARM handhelds), NextUI

## What it does

- Connects to your RomM instance using a [Client API Token](client-api-tokens.md).
- **Pulls** ROMs from RomM to the handheld's SD card, organised into muOS / NextUI's expected folder layout.
- **Pushes** saves and states back to RomM when you finish a session.
- **Schedules** sync runs: on idle, on session end, or on a cron.
- Works fully offline between syncs; the handheld doesn't need RomM to play.

## Why Grout (and not Argosy)?

- **[Argosy](argosy.md)** is Android-native. Good for Android handhelds (Retroid Pocket running Android, phones).
- **Grout** is for non-Android Linux handhelds. muOS and NextUI are Linux, not Android. Argosy's APK won't install.

Same underlying protocol; different client for different OS.

## Installing

### On muOS

1. Grab the latest `.muxapp` release from [GitHub Releases](https://github.com/rommapp/grout/releases/latest).
2. Copy to `/mnt/mmc/ARCHIVE/` on the device (USB, SD swap, or SSH).
3. Launch **Archive Manager** from the Applications menu.
4. Select the Grout `.muxapp` → install.
5. After install, find **Grout** under Applications.

### On NextUI

1. Download the NextUI-flavoured release from the same releases page.
2. Follow NextUI's standard app install flow (paths differ by device; see NextUI docs).

## First-time setup

1. Launch Grout on the handheld.
2. Enter your RomM URL.
3. **Pair Device**: Grout displays an 8-digit code.
4. On any device already signed into RomM, navigate to **Profile → Client API Tokens → + New Token** → create a new token → **Pair Device** → enter the code shown on Grout.
5. Grout receives the token, confirms pairing, and fetches your library metadata.

Details on the pairing flow in [Client API Tokens](client-api-tokens.md).

## Using Grout

### Browse

Grout's main view lists platforms. Select one to see available ROMs. Metadata (titles, cover art) is pulled live from RomM.

### Download ROMs

Select a ROM → **Download**. Grout pulls the file to the expected location on the SD card, so muOS / NextUI's native launcher sees it on next refresh.

Bulk select for multi-file downloads, useful for pulling a whole collection at once.

### Sync cadence

Grout → Settings → Sync:

- **Pull** cadence: how often to check RomM for new ROMs (default: manual; can set to every N minutes when on Wi-Fi).
- **Push** cadence: how often to upload saves (default: on session end).
- **Full sync**: manual; triggers a full bidirectional sync right now.

### What pushes back to RomM

- **Save files.** Once a session ends, Grout uploads any changed saves to RomM.
- **Save states.** Same, if enabled in settings.
- **Play session records.** Start/end times for the **Continue Playing** ribbon and per-ROM playtime on RomM.

## Permissions and access

Grout uses your Client API Token for all API calls. Token scopes:

- `roms.read`, `platforms.read`, `collections.read`: to browse.
- `assets.read`, `assets.write`: to sync saves.
- `devices.read`, `devices.write`: to register as a device.
- `firmware.read`: if you're syncing firmware too.

Scope the token narrowly when creating: default scopes are fine for most users, but an admin shouldn't hand Grout `users.write` just because the token-creation page offers it.

## SSH sync (operator-side)

If you want Grout to pull from RomM over SSH rather than HTTPS (e.g. on a trusted LAN with no reverse proxy) see [SSH Sync](../administration/ssh-sync.md) for the server-side config. Grout supports both modes, selectable in Settings → Connection.

## Troubleshooting

- **Can't see the handheld's Wi-Fi on RomM's network.** Make sure both are on the same SSID / VLAN.
- **Token invalid.** Re-pair; token was revoked or expired.
- **Saves aren't syncing.** Check the sync cadence is set to something other than "never", and that the handheld actually has network during the sync window.
- **"Device not registered".** The pairing step wasn't completed. Re-run pairing from scratch.

More in [Device Sync Troubleshooting](../troubleshooting/sync.md).

## See also

- [Client API Tokens](client-api-tokens.md): token and pairing flow reference.
- [Device Sync Protocol](device-sync-protocol.md): wire-level protocol.
- [SSH Sync](../administration/ssh-sync.md): operator-side SSH config.
- [rommapp/grout](https://github.com/rommapp/grout): source, issues, releases.
