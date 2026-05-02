---
title: Downloads
description: Download ROMs to your local device
---

# Downloads

## How downloads work

Downloads stream directly from disk with no temp file, no copy, and no packaging delay, so large ROMs and multi-disc sets download just as quickly as small ones.

For multi-file games (folder-based), the bundled nginx is built with `mod_zip`, which streams a zip archive over HTTP without ever materialising it on disk. The browser sees a zip download start immediately with no "packaging…" step, regardless of the folder size. The same applies to bulk downloads of multiple ROMs, where memory doesn't grow with selection size.

## Auth

Download URLs require either a session cookie or a bearer token by default. Two patterns for programmatic / third-party use:

### Client API tokens (preferred)

Issue a [Client API Token](../developers/client-api-tokens.md) and pass it as a bearer:

```bash
curl -H "Authorization: Bearer rmm_..." \
     -o mario.sfc \
     https://demo.romm.app/api/roms/123/content/mario.sfc
```

### Disabling auth on download endpoints

Some third-party tools (a dumb emulator loading a ROM by URL, a homebrew Switch app) can't send a bearer token. For those, admins can turn auth off on download endpoints:

```yaml
environment:
    - DISABLE_DOWNLOAD_ENDPOINT_AUTH=true
```

This makes ROM and firmware download URLs work unauthenticated.

<!-- prettier-ignore -->
!!! danger "Only enable this behind upstream auth"
    This flag makes your library world-downloadable from whatever URL serves it. Only set it when you have authentication at the reverse-proxy layer (Authelia, Cloudflare Access, an IP allowlist, a VPN).

## Nintendo 3DS direct install

The 3DS built-in QR scanner can install compatible `.cia` files directly from a URL. RomM produces compatible QR codes, so a 3DS with FBI (or another CIA installer) can install over the air given network access to your instance and either basic-auth on the 3DS side or `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` behind upstream auth.

## Streaming to an emulator

Some emulators take an HTTP URL directly. With `DISABLE_DOWNLOAD_ENDPOINT_AUTH=true` and a reverse proxy that restricts access, you can set up truly remote ROM loading from a handheld over Wi-Fi.

## Download history

Downloads aren't logged for privacy reasons, so use your reverse proxy's access log if you need to audit.

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
