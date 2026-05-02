---
title: Uploads
description: Uploading ROMs
---

# Uploads

<!-- prettier-ignore -->
!!! tip "Prefer direct file transfer for ROMs"
    Copying or moving ROMs straight into the right platform folder under `/romm/library` (via FTP, SFTP, SMB, `rsync`, or your NAS file manager) is more reliable than uploading through the web UI, especially for large or multi-file games. The web UI uploader works, but it's bottlenecked by your browser, the reverse proxy, and any chunked-upload edge cases.

## What you can upload

| Type              | Permission       | Details                                                              |
| ----------------- | ---------------- | -------------------------------------------------------------------- |
| **ROMs**          | Admin, Editor    | Goes to the correct platform folder in `/romm/library`.              |
| **Firmware/BIOS** | Admin, Editor    | See [Firmware Management](../administration/firmware-management.md). |
| **Saves**         | Self (own games) | Per-ROM, per-user.                                                   |
| **States**        | Self (own games) | Per-ROM, per-user, with optional screenshot attached.                     |
| **Screenshots**   | Self (own games) | Per-ROM, per-user.                                                   |
| **Manuals**       | Admin, Editor    | PDF, becomes the Manual tab content.                                 |
| **Cover art**     | Admin, Editor    | Replaces the provider-fetched cover.                                 |

## ROM uploads

### Large uploads (chunked)

Files over 64 MB are uploaded in chunks. The server:

1. Opens an upload session (`POST /api/roms/upload/start`).
2. Streams chunks (`PUT /api/roms/upload/{id}`) of 64 MB each.
3. Finalises the upload (`POST /api/roms/upload/{id}/complete`), which assembles the file and indexes it.

A browser refresh mid-upload cancels the session and cleans up partial data.

### Multi-file uploads

Multi-file uploads (e.g. multi-disc games) aren't supported via the UI. Instead, copy the files directly into the correct platform folder, then run a scan to pick them up. For example, a two-disc PSX game would have `game_disc1.iso` and `game_disc2.iso` copied into `/romm/library/psx/game/`, then a Quick scan run to match them.

## Troubleshooting

- **`413 Request Entity Too Large`**: your reverse proxy or ingress is capping body size (see [Reverse Proxy](../install/reverse-proxy.md) for the `client_max_body_size 0`/`proxy-body-size: "0"` fix).
- **Upload progresses then fails at 99%**: the finalise step timed out. Usually reverse-proxy read timeout is too tight, so raise it.
