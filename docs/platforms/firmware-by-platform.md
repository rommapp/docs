---
title: Firmware by Platform
description: Per-platform firmware/BIOS requirements for in-browser play.
---

# Firmware by Platform

This page lists the firmware RomM's EmulatorJS cores need for each platform. For the admin-side workflow (uploading, managing, bundling multi-file firmware), see [Firmware Management](../administration/firmware-management.md).

<!-- prettier-ignore -->
!!! note "Legality is your problem"
    RomM does not ship firmware. Legality of obtaining firmware varies by jurisdiction and by whether you own the hardware. The project can't help you acquire BIOS files.

## Platforms that need firmware

| Platform                         | Folder slug        | Required files                                                                     | Notes                                                                   |
| -------------------------------- | ------------------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **PlayStation (PSX)**            | `ps`               | `scph1001.bin` (US), `scph5501.bin` (US), `scph5502.bin` (EU), `scph7502.bin` (JP) | At least one region BIOS required.                                      |
| **Saturn**                       | `saturn`           | `saturn_bios.bin`, optional `mpr-17933.bin` (EU)                                   | Bundle both in a zip.                                                   |
| **Sega CD / Mega CD**            | `segacd`           | `bios_CD_U.bin` (US), `bios_CD_E.bin` (EU), `bios_CD_J.bin` (JP)                   | Region depends on your games.                                           |
| **Game Boy Advance**             | `gba`              | `gba_bios.bin`                                                                     | Optional. Games run without it, but accurate emulation needs it.        |
| **Nintendo DS**                  | `nds`              | `bios7.bin`, `bios9.bin`, `firmware.bin`                                           | All three are needed.                                                   |
| **Atari Lynx**                   | `lynx`             | `lynxboot.img`                                                                     |                                                                         |
| **Neo Geo Pocket / Color**       | `ngp` / `ngpc`     | `neopop.rom`                                                                       | Bundle as zip.                                                          |
| **Amiga**                        | `amiga`            | Kickstart ROMs (various)                                                           | `puae` core. Kickstart 1.2, 1.3, 3.1 depending on title. Bundle as zip. |
| **ColecoVision**                 | `colecovision`     | `coleco.rom`                                                                       |                                                                         |
| **Intellivision**                | `intellivision`    | `exec.bin`, `grom.bin`                                                             | Bundle both.                                                            |
| **3DO**                          | `3do`              | `panafz10.bin` (or similar region BIOS)                                            |                                                                         |
| **PC Engine CD / TurboGrafx-CD** | `pcecd` / `tg16cd` | `syscard3.pce`                                                                     |                                                                         |
| **Dreamcast**                    | `dc`               | `dc_boot.bin`, `dc_flash.bin`                                                      | EmulatorJS Dreamcast support is limited, so results vary.               |
| **Atari 5200**                   | `atari5200`        | `5200.rom`                                                                         |                                                                         |
| **Atari 7800**                   | `atari7800`        | `7800 BIOS (U).rom`                                                                |                                                                         |

For cores + platforms not in this table (most Nintendo consoles such as NES, SNES, N64, plus Sega Genesis, Atari 2600, Game Boy, most home computers), **no firmware is needed**.

## Bundling multi-file firmware

Several platforms need multiple files (DS, Amiga, Saturn with region BIOS, Neo Geo Pocket). Pack all the files into a single `.zip` and upload it through the Firmware button on the platform view. EmulatorJS unpacks automatically.

See [Firmware Management](../administration/firmware-management.md).

## Where firmware goes on disk

Depends on your [folder structure](../getting-started/folder-structure.md):

- **Structure A**: `/romm/library/bios/{platform-slug}/`
- **Structure B**: `/romm/library/{platform-slug}/bios/`

So PSX BIOS goes in `bios/ps/` (A) or `ps/bios/` (B).

## File name requirements

Emulator cores look for **specific filenames**. If you rename `scph1001.bin` to something else, PSX won't boot.

Common mistakes:

- Upper vs lower case: most cores are case-sensitive. Use exact case from the table above.
- Extensions: `.bin` vs `.rom` vs `.img` depend on the core. Don't rename.
- Version suffixes: `scph1001 (US) v4.4.bin` won't load. It has to be `scph1001.bin`.

If you're not sure what name a core expects, check the [upstream EmulatorJS systems docs](https://emulatorjs.org/docs/systems/) or load the game with `emulatorjs.debug: true`. The browser console will tell you what file it tried to load.

## Getting firmware

Your options (jurisdiction-dependent):

- **Dump from real hardware you own.** The cleanest answer.
- **Community archives.** Not linked here. The RomM project doesn't host these and doesn't recommend specific sources.
- **Official emulator bundles.** Some modern emulators ship with (or include a button to download) BIOS files. If you bought one, it's yours to use.

## Verifying integrity

Firmware is hash-verified by the emulator: a wrong hash means the file won't load. Quick CLI check:

```sh
sha1sum scph1001.bin
# cbc7bad7bae8de7f6cfb49f1018ca55e8ab0c50a  scph1001.bin
```

Known-good hashes for common BIOS files are documented on [No-Intro](https://datomatic.no-intro.org/) and [Redump](http://redump.org/).

## See also

- [Firmware Management](../administration/firmware-management.md): admin-side upload and lifecycle.
- [Supported Platforms](supported-platforms.md): catalogue with firmware-required flag.
- [In-Browser Play Troubleshooting → "Firmware required"](../troubleshooting/in-browser-play.md#firmware-required): diagnostic.
- [EmulatorJS systems reference](https://emulatorjs.org/docs/systems/): upstream firmware requirements per core.
