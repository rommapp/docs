---
title: Scanning & Watcher
description: Scanning your library, scan modes, and the filesystem watcher
---

# Scanning & Watcher

RomM keeps its catalogue in sync with your filesystem through three mechanisms:

1. **Manual scans** you trigger through the web UI
2. **Scheduled scans** (default: nightly) run by the task runner
3. **The filesystem watcher** reacting to files landing in or leaving your library

All three share the same scan engine and the same set of **scan modes**.

## Scan modes

Every scan picks one mode. Modes differ in what they touch, so use the most-targeted mode that accomplishes what you want.

| Mode              | What it does                                                                                                  | When to use                                                                               |
| ----------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **New Platforms** | Only scans platform folders not already in the DB.                                                            | After mounting a new ROM set (very fast).                                                 |
| **Quick**         | Adds new games, and reconciles the files of games it already knows with what is on disk. No metadata refresh. | Default for scheduled runs and the watcher.                                               |
| **Unmatched**     | Re-runs metadata matching against ROMs currently missing external IDs.                                        | After adding a new metadata provider, or when some titles didn't match on the first scan. |
| **Update**        | Re-fetches metadata for all already-matched ROMs.                                                             | When metadata providers have meaningfully changed (e.g. IGDB restructured).               |
| **Hashes**        | Recalculates CRC/MD5/SHA1 hashes.                                                                             | After upgrading from a version that didn't hash or when you suspect file corruption.      |
| **Complete**      | Full rescan, recalculating hashes and re-fetching metadata for everything.                                    | Rarely, since it takes a long time.                                                       |

You can further scope a scan to specific **platforms** and specific **metadata providers**, useful when only one provider has changed (e.g. just enabled Hasheous → Unmatched scan, Hasheous selected, on all platforms).

## Manual scans

A manual scan can be scoped to specific platforms and a chosen subset of metadata providers, and hashing can be skipped (helpful on low-power hosts). A running scan survives browser refreshes, and the log streams over a websocket so multiple users can watch the same scan in progress.

## Scheduled scans

Configured via env vars (full table in [Scheduled Tasks](scheduled-tasks.md)):

| Variable                | Default     | Purpose                                                                                                    |
| ----------------------- | ----------- | ---------------------------------------------------------------------------------------------------------- |
| `SCHEDULED_RESCAN_CRON` | `0 3 * * *` | Cron expression for the scheduled library scan, which runs a **Quick** scan                                |
| `SCAN_TIMEOUT`          | `14400`     | Hard cap in seconds, after which the scan is killed and the clients watching it are told why               |
| `SCAN_WORKERS`          | `4`         | How many ROMs a scan processes at once, raised from `1`                                                    |
| `SEVEN_ZIP_TIMEOUT`     | `60`        | Per-archive timeout in seconds for `.7z` extraction during scan, raise it if scanning huge compressed sets |

Scans run on their own queue and worker, so a long library scan no longer blocks the shorter background tasks behind it.

To disable scheduled scans entirely, either unset the cron or set it to something unreachable (`SCHEDULED_RESCAN_CRON=0 0 31 2 *`).

## Filesystem watcher

The watcher tails your library folder and schedules scans in response to file events (files added, moved, or deleted). It's off by default, so enable it with:

```yaml
environment:
    - ENABLE_RESCAN_ON_FILESYSTEM_CHANGE=true
    - RESCAN_ON_FILESYSTEM_CHANGE_DELAY=5 # minutes before acting on an event
```

Behaviour:

- Watches `/romm/library` (and everything under it) recursively
- Debounces bursts of events: the delay (default 10 seconds) lets a large `cp` or `rsync` settle before scanning.
- Batches scans intelligently: many events → a single consolidated scan, not one scan per file
- Ignores content modifications and metadata-only changes, caring only about files appearing or disappearing (not `chmod`)
- Skips OS noise (`.DS_Store`, `Thumbs.db`, `.tmp`, etc.)
- If a whole new platform folder appears, switches to a **New Platforms** scan to pick it up cleanly

### When **not** to enable the watcher

- **Slow/high-latency filesystems** (SMB mounts, rclone mounts, anything not local disk): the watcher reacts to every event, flaky mounts generate a lot of them, so use scheduled scans instead.
- **Libraries under active write load from other tools** (e.g. IGIR constantly tagging files): the watcher will re-scan on every change, at best noisy and at worst a scan loop.

### Watcher vs scheduled scan

|                              | Watcher                 | Scheduled scan           |
| ---------------------------- | ----------------------- | ------------------------ |
| Latency                      | Seconds                 | Up to your cron interval |
| CPU cost                     | Only when files change  | Constant cadence         |
| Works over SMB/NFS           | Flakily                 | Reliably                 |
| Catches renames              | Yes                     | Yes                      |
| Survives a container restart | Yes, re-arms on startup | Yes                      |

You can run both, where the watcher handles day-to-day additions, and the scheduled scan is a safety net.

## What gets excluded

Scans respect the `exclude:` tree in [`config.yml`](../reference/configuration-file.md):

```yaml
exclude:
    platforms:
        - steam # skip entire platform folder
    roms:
        single_file:
            extensions: [nfo, txt, bak] # single files with these exts
            names: ["*.sample.*"] # Unix glob patterns
        multi_file:
            names: [extras] # folder names to skip
            parts:
                names: [thumb.png] # files inside multi-file dirs
                extensions: [nfo]
```

Anything you list is **added** to RomM's own defaults rather than replacing them, so the system folders and the frontend media folders stay excluded whether or not you name them. Full schema in [Configuration File](../reference/configuration-file.md).

## Platform folder names

A platform folder has to resolve to a [known slug](../platforms/supported-platforms.md). The folder names **Batocera, RetroBat and ES-DE** use resolve on their own, so a library laid out by one of those frontends needs no configuration. Map anything else with [`system.platforms`](../reference/configuration-file.md#systemplatforms).

## Title ids read from the binary

On the platforms that have one, a scan reads the game's **native title id** straight out of its binary: PSX, PS2, PS3, PSP, PS Vita, Switch, 3DS, Wii, Wii U, GameCube, Dreamcast, Xbox and Xbox 360. That id does two jobs. It identifies a game on the platforms RomM doesn't hash, which is what lets a moved or renamed file keep its saves and collections, and it tells RomM where the game writes its saves so device sync knows what to look for.

Switch headers are encrypted, so a Switch file needs `prod.keys` available for its id to be read, and [`filesystem.embed_switch_title_ids`](../reference/configuration-file.md#filesystemembed_switch_title_ids) can write the id back into the filename. Turn the whole read off with [`filesystem.skip_title_id_extraction`](../reference/configuration-file.md#filesystemskip_title_id_extraction).

## Region and language preference

Also in `config.yml`:

```yaml
scan:
    priority:
        region: [us, wor, ss, eu, jp]
        language: [en, fr]
```

When a metadata provider returns multiple regional variants (Japanese cover, US cover, European cover…), we pick according to this order, and the same goes for localised titles.

## Metadata source priority

Who wins when two providers disagree is covered in [Metadata Providers](../getting-started/metadata-providers.md#priority-and-conflict-resolution), though the short version is `scan.priority.metadata` and `scan.priority.artwork` in `config.yml`.

## Troubleshooting

Scans that hang, miss files, or match weirdly: [Scanning Troubleshooting](../troubleshooting/scanning.md).
