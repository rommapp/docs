---
title: Downloads
description: Download ROMs to your local device
---

# Downloads

## How downloads work

Downloads stream directly from disk with no temp file, no copy, and no packaging delay, so large ROMs and multi-disc sets download just as quickly as small ones.

For multi-file games (folder-based), the bundled nginx is built with `mod_zip`, which streams a zip archive over HTTP without ever materialising it on disk. The browser sees a zip download start immediately with no "packaging…" step, regardless of the folder size.

## Auth

Download URLs require either a session cookie or a bearer token by default. Two patterns for programmatic/third-party use:

### Client API tokens (preferred)

Issue a [Client API Token](../developers/client-api-tokens.md) and pass it as a bearer:

```bash
curl -H "Authorization: Bearer rmm_..." \
     -o mario.sfc \
     https://demo.romm.app/api/roms/123/content/mario.sfc
```

### Disabling auth on download endpoints

Some third-party tools (like a dumb emulator loading a ROM by URL or a homebrew Switch app) can't send a bearer token. For those, admins can disable auth on download endpoints:

```yaml
environment:
    - DISABLE_DOWNLOAD_ENDPOINT_AUTH=true
```

This makes ROM and firmware download URLs work unauthenticated.

<!-- prettier-ignore -->
!!! danger "Only enable this behind upstream auth"
    This flag makes your library world-downloadable from whatever URL serves it. Only set it when you have authentication at the reverse-proxy layer (Authelia, Cloudflare Access, an IP allowlist, or a VPN).

## Downloading in another format

When an admin turns on [download conversion](../administration/library-conversion.md#download-conversion), a single-file game can be downloaded as any format rom-converto can produce from it, such as a `.zso` or `.iso` of a PSP game stored as CHD. The web UI lists these formats as "Download as" on the game page, and the same list is in the `download_formats` field of a game's API response.

API clients ask for one with `?format=` on the download URL, listing every format they can read in order of preference:

```bash
curl -H "Authorization: Bearer rmm_..." \
     -o game.iso \
     "https://demo.romm.app/api/roms/123/content/game.chd?format=zso,iso"
```

The stored file is served as-is when its format is in the list. Otherwise it's converted, with a `202` and a `Retry-After` header while the conversion runs, and a `406` when none of the listed formats can be produced. Converted copies are cached, so the next download of the same format is immediate. Only signed-in users can start a conversion.

## Downloads and player loads

The download endpoint takes a `purpose` query parameter, `download` (the default) or `play`. In-browser players send `purpose=play` when they fetch a game to run it, so the [audit log](../administration/audit-log.md) records a player load rather than a download, though the file served is the same.

## Nintendo 3DS direct install

The 3DS built-in QR scanner can install compatible `.cia` files directly from a URL. RomM produces compatible QR codes, so a 3DS with FBI (or another CIA installer) can install over the air given network access to your instance and either basic-auth on the 3DS side or `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` behind upstream auth.

## Streaming to an emulator

Some emulators take an HTTP URL directly. With `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` and a reverse proxy that restricts access, you can load ROMs remotely from a handheld over Wi-Fi.

## Troubleshooting

- **Download stalls at N%**: usually reverse-proxy buffering, which spools each in-flight download to a temp file and can fill the proxy container's disk (see [Reverse Proxy → Nginx Proxy Manager](../install/reverse-proxy.md#nginx-proxy-manager) for the buffering and timeout settings).
- **Multi-file zip download is corrupt**: the disk may have filled up during streaming, or the nginx mod_zip build is broken. Check `docker logs romm | grep mod_zip`.
