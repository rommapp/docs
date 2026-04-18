---
title: Your First Scan
description: Populate a fresh RomM install by scanning the library for the first time.
---

# Your First Scan

You've got RomM running ([Quick Start](quick-start.md)), your ROMs are laid out correctly ([Folder Structure](folder-structure.md)), and metadata credentials are configured ([Metadata Providers](../administration/metadata-providers.md)). Time to let RomM catalogue everything.

## Before you hit scan

A fifteen-second check that saves hours:

- **Library is mounted**: on the host, `ls /path/to/library` should show your `roms/` (or per-platform) folders. If it doesn't, the mount is wrong.
- **At least one metadata provider is configured**: RomM will scan without one, but every game comes back "unmatched" and you'll have nothing useful to look at.
- **The Setup Wizard is done**: if RomM is still showing the wizard, finish that first. The first user becomes Admin.

## Run the scan

1. Click **Scan** in the sidebar.
2. Leave all platforms checked (they're auto-discovered from your folders).
3. Leave all configured providers checked.
4. Leave the mode as the default.
5. Click **Start Scan**.

The page switches to live mode:

- A **log** on the right streams everything the scanner is doing: file hashed, provider queried, match found or not.
- Per-platform **accordion panels** show counts update live: total found, matched, unmatched.
- You can click a **matched ROM** while the scan is still running to see what metadata RomM pulled, with no need to wait for the full run.

First scans on big libraries take a while. Expect ~1 second per ROM with a fast network to IGDB/ScreenScraper, and hashing (which runs unless you disabled it) adds IO time proportional to file size.

## What "matched" means

For each ROM the scanner:

1. **Computes hashes** (CRC32, MD5, SHA1, plus RetroAchievements-specific hashes).
2. **Hits the configured metadata providers** in priority order. First provider to recognise the file (by hash or filename) becomes the initial match.
3. **Writes the DB entry** with title, cover, description, release date, and anything else the winning provider returned.
4. **Merges overlay data** from other providers: RetroAchievements progression, HowLongToBeat completion times, SteamGridDB alternate covers if you've asked.

An **unmatched** ROM means no provider recognised it. Common causes:

- Filename is too generic (`game.gba`).
- Bad rip, intro / patch applied, or a regional variant no provider has indexed.
- Platform folder misnamed: the scanner queries providers scoped to the detected platform, so wrong platform = no results.
- Metadata provider credentials wrong or rate-limited: check the scan log for errors.

Most of these are fixable. See [Scanning Troubleshooting](../troubleshooting/scanning.md).

## When the scan finishes

Click the **RomM logo** (top-left) to go home. You should see:

- Platform cards for each folder it scanned.
- A **Recently Added** carousel on the dashboard.
- A **Continue Playing** section: empty until you play something.

From here, typical next steps:

- **Browse**: click a platform card, flip through the grid.
- **Fix unmatched ROMs**: rename or re-tag, then re-run an **Unmatched** scan to pick them up. See [Scanning & Watcher](../administration/scanning-and-watcher.md#scan-modes).
- **Tweak priorities**: if ScreenScraper's covers are nicer than IGDB's for your library, reorder `scan.priority.artwork` in [`config.yml`](../reference/configuration-file.md).
- **Add more users**: [Invitations & Registration](../administration/invitations-and-registration.md).

## Skip to a targeted scan

If you're adding ROMs later and don't want a full rescan:

- **New Platforms**: only scans folders RomM hasn't seen before. Fast.
- **Quick**: skips ROMs already catalogued. Good default for "I added a few games".
- **Unmatched**: re-runs matching against ROMs without a provider ID. Good after adding a metadata provider.

All six scan modes are documented in [Scanning & Watcher](../administration/scanning-and-watcher.md#scan-modes).

## Automation

Don't want to keep clicking Scan?

- **Scheduled scans** run nightly by default. Tune with `SCAN_INTERVAL_CRON`.
- **The filesystem watcher** can auto-scan when files appear or disappear. Enable with `WATCHER_ENABLED=true`. Details and tradeoffs in [Scanning & Watcher](../administration/scanning-and-watcher.md).

## It's working: what next?

Back to the [Introduction](../index.md) to pick what you want to do next: set up users, fine-tune admin settings, or just dive in and play. If something's wrong, start with [Scanning Troubleshooting](../troubleshooting/scanning.md).
