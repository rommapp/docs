---
title: Feeds
description: Every URL-feed endpoint RomM exposes for third-party installers and frontends.
---

# Feeds

RomM exposes URL feeds for several homebrew installers and frontends. Each feed is a JSON / CSV / XML representation of a filtered subset of your library in the format the target tool expects.

Feeds are **read-only**. They expose download URLs back to RomM's own `/api/...` endpoints for the actual file transfer.

## Endpoint catalogue

| Feed                     | URL                           | Purpose                                                                       |
| ------------------------ | ----------------------------- | ----------------------------------------------------------------------------- |
| **Tinfoil**              | `/api/feeds/tinfoil`          | Nintendo Switch `.nsp` / `.xci` installer. [Setup →](../ecosystem/feed-clients.md#tinfoil) |
| **pkgi (PS Vita games)** | `/api/feeds/pkgi/psvita/game` | PS Vita `.pkg` installer. [Setup →](../ecosystem/feed-clients.md#pkgj)                     |
| **pkgi (PS Vita DLCs)**  | `/api/feeds/pkgi/psvita/dlc`  | Same, DLC content.                                                                         |
| **pkgi (PSP games)**     | `/api/feeds/pkgi/psp/game`    | PSP `.pkg` installer.                                                                      |
| **pkgi (PSP DLCs)**      | `/api/feeds/pkgi/psp/dlc`     | Same, DLC content.                                                                         |
| **fpkgi (PS4)**          | `/api/feeds/fpkgi/ps4`        | PS4 `.pkg` installer. [Setup →](../ecosystem/feed-clients.md#fpkgi)                        |
| **fpkgi (PS5)**          | `/api/feeds/fpkgi/ps5`        | PS5 `.pkg` installer.                                                                      |
| **Kekatsu (NDS)**        | `/api/feeds/kekatsu/nds`      | Nintendo DS multiboot loader. [Setup →](../ecosystem/feed-clients.md#kekatsu)              |
| **WebRcade**             | `/api/feeds/webrcade`         | Browser-based retro frontend. [Setup →](../ecosystem/feed-clients.md#webrcade)             |

Plus legacy `pkgj` formats for individual platforms:

| Feed         | URL                      |
| ------------ | ------------------------ |
| PKGj PSX     | `/api/feeds/pkgj/psx`    |
| PKGj PS Vita | `/api/feeds/pkgj/psvita` |
| PKGj PSP     | `/api/feeds/pkgj/psp`    |

## Authentication

All feeds respect `DISABLE_DOWNLOAD_ENDPOINT_AUTH`:

- **`DISABLE_DOWNLOAD_ENDPOINT_AUTH=false`** (default, secure): feeds require basic auth. Most clients (Tinfoil, pkgj, fpkgi) can send basic auth in their URL config.
- **`DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`**: feeds are public. Use when RomM is behind upstream auth (reverse proxy with auth, VPN).

See [Authentication → Download-endpoint auth bypass](../administration/authentication.md#download-endpoint-auth-bypass) for the full security discussion.

## Response formats

### JSON feeds

Most feeds return JSON: Tinfoil, fpkgi, WebRcade.

```json
{
  "success": true,
  "files": [
    {
      "url": "https://demo.romm.app/api/roms/1234/content/mario.nsp",
      "title": "Super Mario Odyssey",
      "size": 4500000000,
      "titleid": "0100000000010000",
      ...
    }
  ]
}
```

### CSV feeds

pkgi uses CSV per upstream's format: one line per game:

```csv
psvita,PCSA00003,Unknown,Game,1.0,https://demo.romm.app/...,md5=...,52428800
```

### Format per feed

Each feed's exact schema matches what its client expects. Don't call feeds by accident from other tools. Tinfoil can't parse WebRcade JSON, and vice versa.

## Filtering

Most feeds filter by file extension automatically:

- **Tinfoil** → `.nsp`, `.xci`, `.nsz`, `.xcz`
- **pkgi** / **fpkgi** → `.pkg`
- **Kekatsu** → `.nds`
- **WebRcade** → any extension the WebRcade emulator supports

Games not matching the expected extension are silently skipped, not reported as missing.

## Performance notes

Feeds query the whole library for the target platform on every request. For large libraries that's measurable but not slow (< 1s typically). Clients generally cache feed responses, so don't hit the feed in a tight loop.

## Platform slugs

The `{platform_slug}` in feed URLs (`fpkgi/{platform}`, `kekatsu/{platform}`) takes RomM's canonical platform slug. See [Supported Platforms](../platforms/supported-platforms.md) for the full list.

If you've remapped your folder names to canonical slugs via [`system.platforms`](configuration-file.md#systemplatforms), use the canonical slug in the feed URL, not your folder name.

## Adding a new feed format

If you want RomM to expose a feed format it doesn't currently support:

1. Check the [backend/routers/feeds/](https://github.com/rommapp/romm/tree/master/backend/routers) directory for existing implementations as templates.
2. Open an issue describing the target client, its feed format, and any authentication requirements.
3. Ideally, open a PR. Feed endpoints are usually small: a few dozen lines of Python to filter + format.

## See also

- [Ecosystem](../ecosystem/index.md): per-client setup guides
- [Authentication](../administration/authentication.md): auth options affecting feeds
- [API Reference](../developers/api-reference.md): full endpoint catalogue
