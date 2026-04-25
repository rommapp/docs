---
title: Server Stats
description: "The numbers Mason! What do they mean?"
---

# Server Stats

**Administration → Server Stats** is an admin-only page that reports what's on disk and in the catalogue.

## What's shown

### Top-line counts

| Metric          | What it counts                                                                    |
| --------------- | --------------------------------------------------------------------------------- |
| **Platforms**   | Every platform RomM has seen at least one ROM for. Deleted platforms don't count. |
| **Games**       | Total ROM entries. A multi-file game (folder with multiple files) counts as 1.    |
| **Saves**       | User save files across all users.                                                 |
| **States**      | Emulator save states across all users.                                            |
| **Screenshots** | User-uploaded screenshots. Provider-fetched screenshots aren't counted here.      |
| **Size on disk** | Total disk usage of all ROMs, saves, states, and screenshots.                    |

### Per-platform breakdown

Under the summary, it's a table sorted by name, size or game count. For each platform, you can see:

- Game count
- Size on disk (in bytes and by percentage of total)
- Region distribution (how many games tagged USA, Japan, Europe, World, etc.)
- Metadata coverage (how many games have metadata from each provider)

When you want to know "which platform is eating my disk?" or "which platform has the worst match rate?"

## API

The same data is available programmatically:

```http
GET /api/stats
GET /api/stats?include_platform_stats=true
Authorization: Bearer <token>
```

Wire to your monitoring stack via the API rather than scraping the HTML page. See the [API Reference](../developers/api-reference.md).

## Troubleshooting

- **Numbers look stale**: stats are computed on page load, not cached
- **Disk sizes look wrong**: if your compose mounts a path that's smaller than the host dataset (e.g. you mounted a sub-directory), it will only sees that subset
- **"Platform stats couldn't load"**: the DB query timed out on a very large library

For anything else, see [Troubleshooting](../troubleshooting/index.md).
