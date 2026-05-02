---
title: Firmware Management
description: Upload, associate, and serve BIOS/firmware files for emulation.
---

# Firmware Management

Many emulated platforms require BIOS or firmware to boot, or to reach a certain level of stability. RomM tracks firmware files **per platform**, stores them on disk, and serves them to in-browser players (EmulatorJS/Ruffle) and companion apps that request them.

Firmware is **not** ROM. Keep the two separate:

- `/romm/library/roms/`: game ROMs, homebrew, demos, etc.
- `/romm/library/bios/`: system firmware

<!-- prettier-ignore -->
!!! important "Legality varies by jurisdiction"
RomM does not ship games or firmware, and the team cannot help you obtain BIOS files. Always check your local laws and the emulator's documentation for guidance on what you can legally use.

## Ingesting firmware

1. Put the file in the right `bios/` folder (see [Folder Structure](../getting-started/folder-structure.md))
2. Run a scan → Firmware is picked up alongside ROMs
3. Navigate to the platform's gallery and click the `CPU` icon in the top left
4. Firmware files will display at the bottom of the page

## Platform-specific firmware

Every emulator has its own requirements: which files it needs, specific hashes, naming conventions. The [Supported Platforms](../platforms/supported-platforms.md) table flags which platforms need firmware for EmulatorJS playback.

Common examples:

| Platform          | Typical firmware file                             | Where to put it |
| ----------------- | ------------------------------------------------- | --------------- |
| PlayStation (PSX) | `scph1001.bin`, `scph5501.bin`, `scph5502.bin`    | `bios/ps/`      |
| Game Boy Advance  | `gba_bios.bin`                                    | `bios/gba/`     |
| Sega CD           | `bios_CD_U.bin`, `bios_CD_E.bin`, `bios_CD_J.bin` | `bios/segacd/`  |
| Saturn            | `saturn_bios.bin`, `mpr-17933.bin`                | `bios/saturn/`  |
| Nintendo DS       | `firmware.bin`, `bios9.bin`, `bios7.bin`          | `bios/nds/`     |

File naming matters as emulators look for specific filenames. Double-check against the emulator core's documentation if something won't boot.

## Integration with companion apps

Handheld syncers (Grout, Argosy, DeckRommSync) can pull firmware alongside ROMs. They use the same Client API Token auth as for ROMs, so scope the token to include `firmware.read`.

## Backups

Firmware files are user-owned data, so back them up! If you're backing up the `/romm/library` volume, firmware is already covered (see [Backup & Restore](../install/backup-and-restore.md)).
