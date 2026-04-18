---
title: Kekatsu
description: Nintendo DS multiboot loader — install DS games from RomM via custom feed.
---

# Kekatsu

**Kekatsu** is Nintendo DS homebrew for loading games from a custom URL feed. RomM exposes a Kekatsu-compatible feed for its DS library.

New in RomM 5.0.

## Prerequisites

- A Nintendo DS with Kekatsu installed (requires a flashcart or homebrew launcher).
- **RomM reachable from the DS over Wi-Fi** — the DS's Wi-Fi is WEP / old WPA only, so this typically means a dedicated legacy-SSID on your router or a travel router bridging the DS to your modern network.
- DS games in `.nds` format.

## Feed URL

```text
{romm_url}/api/feeds/kekatsu/{platform_slug}
```

For standard DS content, the platform slug is `nds`:

```text
http://192.168.1.100:3000/api/feeds/kekatsu/nds
```

## Configuring Kekatsu

Exact config steps depend on your Kekatsu build; the shared concept is "point the app at this URL and it fetches the manifest". Consult Kekatsu's own docs for the current config-file location.

## File format

`.nds` only. DSi Ware / iQue / other formats aren't listed in the feed.

## Authentication

Kekatsu can send basic auth. Either configure it on the DS side or enable `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` on RomM (see the [Tinfoil download-auth caveat](tinfoil.md#prerequisites)).

## Why the legacy-Wi-Fi hassle

The DS's original Wi-Fi hardware supports WEP and an older WPA variant only. Modern home routers usually don't. Workarounds:

- **Dedicated DS-friendly SSID.** Many routers allow per-SSID security — add a WEP one just for the DS.
- **Travel router in bridge mode.** A cheap travel router configured for WEP uplinks to your main (secure) network.
- **Use a DSi, 3DS, or homebrew replacement driver** — these support modern security.

If none of this is appealing, Kekatsu-over-LAN isn't going to work; fall back to sideloading via flashcart or similar.

## Troubleshooting

- **Feed is empty** — no `.nds` files on the `nds` platform.
- **DS can't see the network** — see the legacy-Wi-Fi section above.
- **Downloads fail** — either network timeout (LAN latency over WEP is rough) or disk space. Retry one game at a time.

## See also

- [Feeds reference](../reference/feeds.md) — all feed endpoints.
- Kekatsu upstream — find via the RomM Discord `#kekatsu` or community links (project moves).
