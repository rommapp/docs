---
title: Your First Scan
description: Populate a fresh install by scanning the library for the first time
---

# Your First Scan

You're up and running ([Quick Start](quick-start.md)), your ROMs are laid out correctly ([Folder Structure](folder-structure.md)), and metadata credentials are configured ([Metadata Providers](../administration/metadata-providers.md)). Time to catalogue everything!

## Before you hit scan

A fifteen-second check that saves hours:

- **Library is mounted**: on the host, `ls /path/to/library` should show your `roms/` (or per-platform) folders. If it doesn't, the mount is wrong.
- **At least one metadata provider is configured**: Scans run without one but every game comes back "unmatched" and you'll have nothing useful to look at.

## Run the scan

1. Click **Scan** in the sidebar.
2. Select the metadata sources you want to hit.
3. Set the mode to Quick Scan
4. Click **SCAN**.

The page switches to a live feed of the scan's progress. You can leave and come back later, or even close the browser and check back in an hour. During the scan:

- Per-platform **accordion panels** show counts update live: total found, matched, unmatched.
- You can click a **matched ROM** while the scan is still running to see the pulled metadata, with no need to wait for the full run.

First scans on big libraries take a while: expect ~4 seconds per ROM with a fast network to IGDB/ScreenScraper, and hashing (which runs unless you disabled it) adds IO time proportional to file size.

## What "matched" means

For each ROM the scanner:

1. **Computes hashes** (CRC32, MD5, SHA1, plus RetroAchievements-specific hashes).
2. **Hits the configured metadata providers** in priority order. First provider to recognise the file (by hash or filename) becomes the initial match.
3. **Writes the DB entry** with title, cover, description, release date, and anything else the providers returned.
4. **Merges overlay data** from other providers: RetroAchievements progression, HowLongToBeat completion times, SteamGridDB alternate covers if you've asked.

An **unmatched** ROM means no provider recognised it, with common causes:

- Filename is too generic (`game.gba`)
- Platform folder misnamed
- Bad rip, intro/patch applied, or a regional variant no provider has indexed
- Metadata provider credentials wrong or rate-limited

Most of these are fixable, see [Scanning Troubleshooting](../troubleshooting/scanning.md).

## When the scan finishes

Click the **logo** (top-left) to go home. You should see:

- Platform cards for each folder it scanned
- A **Recently Added** carousel on the dashboard
- A **Continue Playing** section (empty until you play something)

From here, typical next steps:

- **Browse**: click a platform card, flip through the grid.
- **Fix unmatched ROMs**: rename or re-tag, then re-run an **Unmatched** scan to pick them up. See [Scanning & Watcher](../administration/scanning-and-watcher.md#scan-modes).
- **Tweak priorities**: if ScreenScraper's covers are nicer than IGDB's for your library, reorder `scan.priority.artwork` in [`config.yml`](../reference/configuration-file.md).

## Skip to a targeted scan

If you're adding ROMs later and don't want a full rescan:

- **New Platforms**: only scans folders not seen before, and it's fast.
- **Quick**: skips ROMs already catalogued, a good default for "I added a few games".
- **Unmatched**: re-runs matching against ROMs without a provider ID, ideal after adding a metadata provider.

All six scan modes are documented in [Scanning & Watcher](../administration/scanning-and-watcher.md#scan-modes).
