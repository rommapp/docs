---
title: Downloads
description: Download ROMs from RomM: single, bulk, QR codes, copy-link, and streaming for third-party apps.
---

# Downloads

## Single download

The quick path: hover a game card → click **Download**. Or from the game detail page → **Download** button.

RomM streams the file directly: no temp file on disk, no copy, no waiting for packaging. Large ROMs and multi-disc sets download just as quickly as small ones.

For multi-file games (folder-based), RomM streams a zip on the fly. See [Multi-file downloads](#multi-file-and-bulk-downloads-nginx-mod_zip) below.

## Copy download link

For cases where you want the URL, not the file right now: sending it to another device, pasting into a script, using an external download manager.

Context menu (…) on a game card → **Copy download link**, and the URL is on your clipboard.

Anyone with access to the link and the server can download. By default the link requires your session cookie or a bearer token. See [Third-party download auth](#third-party-download-auth) for the exception.

## QR code

For handheld-to-desktop or desktop-to-phone transfers without typing a URL.

Context menu (…) → **Show QR Code**, then point the other device's camera at the screen.

The QR decodes to the same URL as Copy Link. Same auth rules apply.

## Multi-file and bulk downloads (nginx `mod_zip`)

RomM's nginx is built with `mod_zip`, which streams a zip archive over HTTP without ever materialising the file on disk. Two places this matters:

### Multi-disc / multi-file games

When a game is stored as a folder (multi-disc, game + DLC, game + patch, etc.), clicking **Download** builds a zip on the fly containing the whole folder. The browser sees a zip download start immediately, no "packaging…" delay.

### Bulk download from a gallery

Multi-select ROMs in any gallery (platform view, collection, search results) → toolbar → **Download selected**, producing a single zip with every selected ROM preserved in its platform folder structure.

No practical limit: the zip is streamed, so memory doesn't grow with selection size. Disk I/O and network bandwidth are the actual limits.

## Third-party download auth

Some third-party tools (a dumb emulator loading a ROM by URL, a browser extension, a homebrew Switch app) can't send a bearer token. For those, admins can turn off download-endpoint auth.

```yaml
environment:
  - DISABLE_DOWNLOAD_ENDPOINT_AUTH=true
```

This makes ROM and firmware download URLs work unauthenticated.

!!! danger "Only enable this behind upstream auth"
    This flag makes your library world-downloadable from whatever URL RomM lives at. Only set it when you have authentication at the reverse-proxy layer (Authelia, Cloudflare Access, an IP allowlist, a VPN).

For authenticated programmatic use, a [Client API Token](account-and-profile.md) is the cleaner answer:

```bash
curl -H "Authorization: Bearer rmm_..." \
     -o mario.sfc \
     https://romm.example.com/api/roms/123/content/mario.sfc
```

## Streaming to an emulator

Some emulators can take an HTTP URL directly. Point them at the same URL the Copy Link button produces. With `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` and a reverse proxy that restricts access, you can set up truly remote ROM loading from a handheld over Wi-Fi.

## Download history

Not tracked in 5.0. RomM doesn't log downloads for privacy reasons. Use your reverse proxy's access log if you need to audit.

## Troubleshooting

- **Download stalls at N%**: usually the reverse proxy buffering to disk. See [Reverse Proxy → Nginx Proxy Manager](../install/reverse-proxy.md#nginx-proxy-manager) for the `proxy_max_temp_file_size 0` fix.
- **Multi-file zip download is corrupt**: disk may have filled up during streaming, or the nginx mod_zip build is broken. Check `docker logs romm | grep mod_zip`.
- **Bulk download ends early**: reverse proxy is enforcing a request timeout. Raise `proxy_read_timeout`. See [Kubernetes Troubleshooting](../troubleshooting/kubernetes.md#websockets-disconnect-immediately) for nginx-ingress annotation pattern.

## API

```http
GET  /api/roms/{id}/content/{filename}       # single file, stream
GET  /api/roms/download?ids=1,2,3            # bulk zip stream
HEAD /api/roms/{id}/content/{filename}       # size + content-type without body
```

Requires `roms.read` scope unless `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true`. Full API reference: [API Reference](../developers/api-reference.md).
