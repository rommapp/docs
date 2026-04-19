---
title: fpkgi
description: Install PS4 / PS5 packages from your RomM library via fpkgi homebrew.
---

# fpkgi

[fpkgi](https://github.com/CyberYoshi64/fpkgi) is PS4 / PS5 homebrew for installing `.pkg` packages from custom URL feeds. RomM exposes fpkgi-compatible feeds for its PS4 and PS5 libraries.

New in RomM 5.0. Earlier versions didn't have fpkgi feeds.

## Prerequisites

- **PS4 or PS5** with fpkgi installed (requires CFW / jailbreak, and setup is out of scope here).
- **RomM reachable from the console over Wi-Fi.** LAN simplest.
- Games stored as `.pkg` files. fpkgi, like pkgj, only handles the Sony installer format.

## Feed URL

```text
{romm_url}/api/feeds/fpkgi/{platform_slug}
```

Where `{platform_slug}` is:

- `ps4` for PlayStation 4 content.
- `ps5` for PlayStation 5 content.

Example:

```text
http://192.168.1.100:3000/api/feeds/fpkgi/ps4
```

The feed returns JSON in the fpkgi-expected schema: titles, title IDs, content types, URLs back to RomM for the actual downloads.

## Configuring fpkgi

Exact steps depend on the fpkgi version but the gist:

1. Put RomM's feed URL in fpkgi's config (usually a JSON file on the console, so check fpkgi's own docs).
2. Restart fpkgi.
3. The RomM library appears in fpkgi's browse view.

Consult [fpkgi's README](https://github.com/CyberYoshi64/fpkgi) for the current config-file location and format. The project moves faster than these docs.

## Authentication

The `/api/feeds/fpkgi/` endpoints support basic auth the same way `/api/feeds/pkgi/` does. Either:

- Set basic-auth credentials in fpkgi's config if it supports them, OR
- Set `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` on the RomM server (see the [Tinfoil](tinfoil.md) caveat about public exposure).

## File format: must be `.pkg`

PS4 `.pkg` files specifically, not `.iso`, not compressed. RomM filters to `.pkg` when building the feed. Any other file types are invisible to fpkgi.

## Troubleshooting

- **Feed is empty.** No `.pkg` files on the `ps4` / `ps5` platform. Check your library.
- **Downloads fail with 401.** Auth config mismatch. See Authentication section above.
- **Downloads succeed but install fails.** `.pkg` is for a different firmware version. Not a RomM problem.

## See also

- [Feeds reference](../reference/feeds.md): all feed endpoints.
- [pkgj](pkgj.md): PS Vita / PSP equivalent.
- [fpkgi upstream](https://github.com/CyberYoshi64/fpkgi): installer homebrew.
