---
title: Downloads
description: Download ROMs from RomM to your local device
---

# Downloads

## Single download

The quick path: hover a game card → click **Download**. Or from the game detail page → **Download** button.

The file streams directly, with no temp file on disk, no copy, and no waiting for packaging, so large ROMs and multi-disc sets download just as quickly as small ones.

For multi-file games (folder-based), a stream of a zip on the fly (see [Multi-file downloads](#multi-file-and-bulk-downloads-nginx-mod_zip) below).

## Copy download link

For cases where you want the URL, not the file right now: sending it to another device, pasting into a script, using an external download manager.

Context menu (…) on a game card → **Copy download link**, and the URL is on your clipboard.

Anyone with access to the link and the server can download, though by default the link requires your session cookie or a bearer token (see [Third-party download auth](#third-party-download-auth) for the exception).

## QR code

For handheld-to-desktop or desktop-to-phone transfers without typing a URL.

Context menu (…) → **Show QR Code**, then point the other device's camera at the screen.

The QR decodes to the same URL as Copy Link, and the same auth rules apply.

### Nintendo 3DS direct install

The 3DS built-in QR scanner can install compatible `.cia` files directly from a URL. For supported Nintendo 3DS files, the QR code becomes a one-tap install path:

1. Open the ROM → context menu → **Show QR Code**.
2. On the 3DS, launch FBI (or another CIA installer that accepts QR input).
3. Select **Install from URL** → **Scan QR** → point at your screen.

Same prerequisites as any Copy Link / QR download: the 3DS needs network access to your instance, and the file has to be accessible (either authenticated with basic-auth support on the 3DS side, or `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` behind upstream auth).

## Multi-file and bulk downloads (nginx `mod_zip`)

The bundled nginx is built with `mod_zip`, which streams a zip archive over HTTP without ever materialising the file on disk. Two places this matters:

### Multi-disc / multi-file games

When a game is stored as a folder (multi-disc, game + DLC, game + patch, etc.), clicking **Download** builds a zip on the fly containing the whole folder, and the browser sees a zip download start immediately with no "packaging…" delay.

### Bulk download from a gallery

Multi-select ROMs in any gallery (platform view, collection, search results) → toolbar → **Download selected**, producing a single zip with every selected ROM preserved in its platform folder structure.

No practical limit: the zip is streamed so memory doesn't grow with selection size, and disk I/O and network bandwidth are the actual limits.

## Third-party download auth

Some third-party tools (a dumb emulator loading a ROM by URL, a browser extension, a homebrew Switch app) can't send a bearer token. For those, admins can turn off download-endpoint auth.

```yaml
environment:
    - DISABLE_DOWNLOAD_ENDPOINT_AUTH=true
```

This makes ROM and firmware download URLs work unauthenticated.

<!-- prettier-ignore -->
!!! danger "Only enable this behind upstream auth"
    This flag makes your library world-downloadable from whatever URL serves it. Only set it when you have authentication at the reverse-proxy layer (Authelia, Cloudflare Access, an IP allowlist, a VPN).

For authenticated programmatic use, a [Client API Token](account-and-profile.md) is the cleaner answer:

```bash
curl -H "Authorization: Bearer rmm_..." \
     -o mario.sfc \
     https://demo.romm.app/api/roms/123/content/mario.sfc
```

## Streaming to an emulator

Some emulators can take an HTTP URL directly. Point them at the same URL the Copy Link button produces. With `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` and a reverse proxy that restricts access, you can set up truly remote ROM loading from a handheld over Wi-Fi.

## Download history

Not tracked in 5.0: Downloads aren't logged for privacy reasons, so use your reverse proxy's access log if you need to audit.

## Troubleshooting

- **Download stalls at N%**: usually the reverse proxy buffering to disk (see [Reverse Proxy → Nginx Proxy Manager](../install/reverse-proxy.md#nginx-proxy-manager) for the `proxy_max_temp_file_size 0` fix).
- **Multi-file zip download is corrupt**: disk may have filled up during streaming, or the nginx mod_zip build is broken. Check `docker logs romm | grep mod_zip`.
- **Bulk download ends early**: reverse proxy is enforcing a request timeout. Raise `proxy_read_timeout` (see [Kubernetes Troubleshooting](../troubleshooting/kubernetes.md#websockets-disconnect-immediately) for nginx-ingress annotation pattern).

## API

```http
GET  /api/roms/{id}/content/{filename}       # single file, stream
GET  /api/roms/download?ids=1,2,3            # bulk zip stream
HEAD /api/roms/{id}/content/{filename}       # size + content-type without body
```

Requires `roms.read` scope unless `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`. Full API reference: [API Reference](../developers/api-reference.md).
