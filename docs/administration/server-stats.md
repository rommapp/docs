---
title: Server Stats
description: Read the Server Stats admin page and know what the numbers mean.
---

# Server Stats

**Administration → Server Stats.** Admin-only page that reports what's on disk and in the catalogue. Useful for capacity planning, spotting a runaway platform, and verifying a scan actually persisted data.

## What's shown

### Top-line counts

| Metric | What it counts |
| --- | --- |
| **Platforms** | Every platform RomM has seen at least one ROM for. Deleted platforms don't count. |
| **Games** | Total ROM entries. A multi-file game (folder with multiple files) counts as 1. |
| **Saves** | User save files across all users. |
| **States** | Emulator save states across all users. |
| **Screenshots** | User-uploaded screenshots. Provider-fetched screenshots aren't counted here. |
| **Firmware** | Uploaded BIOS / firmware files. |

### Storage footprint

A breakdown of disk usage by directory:

| Bucket | Maps to | Grows when |
| --- | --- | --- |
| **Library** | `/romm/library` | You add ROMs. Controlled by you, not RomM. |
| **Resources** | `/romm/resources` | Scans fetch cover art, screenshots, manuals. Safe to purge; can be rebuilt from a rescan. |
| **Assets** | `/romm/assets` | Users upload saves, states, screenshots. **Back this up.** |
| **Config** | `/romm/config` | Rarely: you or admins edit `config.yml`. |

### Per-platform breakdown

Under the summary, an expandable table sorted by either ROM count or disk usage. Click a platform to drill into:

- Matched / unmatched count.
- Region distribution (how many games tagged USA, Japan, Europe, World, etc.).
- Language distribution.
- Metadata coverage: how many games have each field populated (cover, description, release date, rating).

Useful for: "which platform is eating my disk?" and "which platform has the worst match rate?"

!!! note "Per-platform stats are opt-in"
    Computing per-platform stats walks the whole DB and costs real time on big libraries. The main stats load fast; per-platform expansion loads on demand.

## What the numbers don't include

- **Disk usage for the database itself**: MariaDB / Postgres data volume isn't reported here. Use `docker system df -v` or your volume backend's native tooling.
- **Redis memory**: same; monitor Redis separately if you're tight on RAM.
- **Per-user storage breakdown**: not exposed in 5.0.

## Using stats for capacity planning

Rule-of-thumb sizes:

| Ratio | Typical value |
| --- | --- |
| Resources / Library | 2-5% on average; higher if you've enabled many metadata providers or run Image Conversion often. |
| Assets / Library | <1% unless you have lots of heavy PSP/PS3 saves. |
| DB size / Games | ~10-50 KB per ROM row, depending on metadata richness. |

If **Resources** is ballooning, run the [Cleanup Orphaned Resources](scheduled-tasks.md#cleanup-orphaned-resources-manual) task. If **Assets** is growing unexpectedly, a user is probably uploading save states for long-form JRPGs; that's fine, just plan for it.

## API

The same data is available programmatically:

```http
GET /api/stats
GET /api/stats?include_platform_stats=true
Authorization: Bearer <token>
```

Wire to your monitoring stack via the API rather than scraping the HTML page. See the [API Reference](../developers/api-reference.md).

## Troubleshooting

- **Numbers look stale**: stats are computed on page load, not cached. Reload. If still stale, the DB connection is degraded; check `docker logs romm 2>&1 | grep -i database`.
- **Disk sizes look wrong**: RomM reports what it sees in `/romm/*`. If your compose mounts a path that's smaller than the host dataset (e.g. you mounted a sub-directory), RomM only sees that subset.
- **"Platform stats couldn't load"**: the DB query timed out. On very large libraries this happens; retry, or raise `SCAN_TIMEOUT_HOURS` (yes, it also gates the stats query).

For anything else: [Troubleshooting](../troubleshooting/index.md).
