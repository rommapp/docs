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

| Mode              | What it does                                                               | When to use                                                                               |
| ----------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **New Platforms** | Only scans platform folders not already in the DB.                         | After mounting a new ROM set (very fast).                                                 |
| **Quick**         | Skips files that already exist in the DB, with no metadata refresh.        | Default for scheduled runs and the watcher.                                               |
| **Unmatched**     | Re-runs metadata matching against ROMs currently missing external IDs.     | After adding a new metadata provider, or when some titles didn't match on the first scan. |
| **Update**        | Re-fetches metadata for all already-matched ROMs.                          | When metadata providers have meaningfully changed (e.g. IGDB restructured).               |
| **Hashes**        | Recalculates CRC/MD5/SHA1 hashes.                                          | After upgrading from a version that didn't hash or when you suspect file corruption.      |
| **Complete**      | Full rescan, recalculating hashes and re-fetching metadata for everything. | Rarely, since it takes a long time.                                                       |

You can further scope a scan to specific **platforms** and specific **metadata providers**, useful when only one provider has changed (e.g. just enabled Hasheous → Unmatched scan, Hasheous selected, on all platforms).

## Manual scans

A manual scan can be scoped to specific platforms and a chosen subset of metadata providers, and hashing can be skipped (helpful on low-power hosts). A running scan survives browser refreshes, and the log streams over a websocket so multiple users can watch the same scan in progress.

## Scheduled scans

Configured via env vars (full table in [Scheduled Tasks](scheduled-tasks.md)):

| Variable             | Default     | Purpose                                                                                                      |
| -------------------- | ----------- | ------------------------------------------------------------------------------------------------------------ |
| `SCAN_INTERVAL_CRON` | `0 0 * * *` | Cron expression for the scheduled library scan. Runs a **Quick** scan by default.                            |
| `SCAN_TIMEOUT`       | `14400`     | Hard cap in seconds: scans that exceed this are killed and logged.                                           |
| `SCAN_WORKERS`       | `1`         | Concurrent worker processes for scanning; leave as auto unless you're tuning.                                |
| `SEVEN_ZIP_TIMEOUT`  | `60`        | Per-archive timeout in seconds for `.7z` extraction during scan; raise if scanning huge compressed ROM sets. |

To disable scheduled scans entirely, either unset the cron or set it to something unreachable (`SCAN_INTERVAL_CRON=0 0 31 2 *`).

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

Full schema in [Configuration File](../reference/configuration-file.md).

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

Who wins when two providers disagree is covered in [Metadata Providers](metadata-providers.md#priority-and-conflict-resolution), though the short version is `scan.priority.metadata` and `scan.priority.artwork` in `config.yml`.

## Troubleshooting

Scans that hang, miss files, or match weirdly: [Scanning Troubleshooting](../troubleshooting/scanning.md).
