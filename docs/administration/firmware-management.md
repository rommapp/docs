---
title: Firmware Management
description: Upload, associate, and serve BIOS/firmware files for emulation.
---

# Firmware Management

Many emulated platforms require BIOS or firmware to boot: PlayStation (SCPH1001), Saturn, Game Boy Advance, Sega CD, and more. RomM tracks firmware files **per platform**, stores them on disk, and serves them to in-browser players (EmulatorJS / Ruffle) and companion apps that request them.

Firmware is **not** ROM. Keep the two separate:

- `/romm/library/roms/`: games you own dumps of.
- `/romm/library/bios/` (Structure A) or `/romm/library/{platform}/bios/` (Structure B): system firmware.

Legality varies by jurisdiction. RomM does not ship firmware and the project cannot help you obtain it.

## Two paths to ingest firmware

### Path 1: drop it in the folder, let the scan pick it up

The usual workflow if you have firmware on disk already.

1. Put the file in the right `bios/` folder (Structure A or B, see [Folder Structure](../getting-started/folder-structure.md)).
2. Run a scan. Firmware is picked up alongside ROMs.
3. It shows up in **Administration → Library Management → Firmware**.

### Path 2: upload through the UI

When you don't have shell access or you're uploading from a different machine.

1. Go to the platform detail page (click a platform card from the home dashboard).
2. Click the **Upload** menu → **Upload Firmware**.
3. Drag and drop the file, or click to browse.
4. RomM puts it in the correct `bios/{platform}/` directory on disk.

Editors and Admins can upload firmware, but Viewers can't (`firmware.write` scope required, see [Users & Roles](users-and-roles.md)).

## Platform-specific firmware

Every emulator has its own requirements: which files it needs, specific hashes, naming conventions. The [Supported Platforms](../platforms/supported-platforms.md) table flags which platforms need firmware for EmulatorJS playback, and a dedicated [Firmware by Platform](../platforms/firmware-by-platform.md) page lists what's needed for the popular ones.

Common examples:

| Platform | Typical firmware file | Where to put it |
| --- | --- | --- |
| PlayStation (PSX) | `scph1001.bin`, `scph5501.bin`, `scph5502.bin` | `bios/ps/` |
| Game Boy Advance | `gba_bios.bin` | `bios/gba/` |
| Sega CD | `bios_CD_U.bin`, `bios_CD_E.bin`, `bios_CD_J.bin` | `bios/segacd/` |
| Saturn | `saturn_bios.bin`, `mpr-17933.bin` | `bios/saturn/` |
| Nintendo DS | `firmware.bin`, `bios9.bin`, `bios7.bin` | `bios/nds/` |

File naming matters: emulators look for specific filenames. Double-check against the emulator core's documentation if something won't boot.

## Listing and deleting firmware

**Administration → Library Management → Firmware** shows every firmware file RomM knows about, grouped by platform. From here you can:

- See file sizes and detected platform.
- Download a firmware file (useful for verifying integrity off-host).
- Delete a firmware entry.

!!! warning "Deleting firmware"
    Deleting from the UI **does** remove the file from disk. If you want to keep the file but unlink it from RomM, move it out of the `bios/` folder first, then rescan.

## API

Firmware has a standard REST surface under `/api/firmware/`:

- `GET /api/firmware`: list (optional `?platform_id=` filter).
- `POST /api/firmware`: upload.
- `GET /api/firmware/{id}/content/{filename}`: download.
- `POST /api/firmware/delete`: bulk delete.

Requires `firmware.read` / `firmware.write` scopes. See the [API Reference](../developers/api-reference.md).

## Integration with in-browser play

When a user launches a platform that requires firmware in EmulatorJS:

1. The player checks RomM for a matching firmware file.
2. If present, it's served directly. No user action required.
3. If missing, the player surfaces an error ("firmware required") and the admin needs to upload one.

Configure which emulator settings to expose to users via `emulatorjs.settings` in [`config.yml`](../reference/configuration-file.md). Details on the player side in [In-Browser Play](../using/in-browser-play.md).

## Integration with companion apps

Handheld syncers (Grout, Argosy, DeckRommSync) can pull firmware alongside ROMs. They use the same Client API Token auth as for ROMs, so scope the token to include `firmware.read`. See [Client API Tokens](../ecosystem/client-api-tokens.md).

## Backups

Firmware is user-owned data: back it up. `/romm/library/bios/` is part of your library mount, so if you're backing up the library volume, firmware is already covered. See [Backup & Restore](../install/backup-and-restore.md).
