---
title: Platforms & Players
description: Everything about the platforms RomM supports: catalogue, custom mappings, emulator tuning, firmware.
---

# Platforms & Players

This section covers:

- **[Supported Platforms](supported-platforms.md)**: the canonical catalogue of every platform RomM ships with. Platform slugs, active metadata providers per platform, EmulatorJS support flag, and firmware requirements.
- **[Custom Platforms](custom-platforms.md)**: how to add platforms RomM doesn't know about, plus custom platform icons.
- **[MS-DOS](ms-dos.md)**: long-form guide to DOS on RomM: `dosbox-pure`, installer ROMs, autorun scripts, known issues.
- **[EmulatorJS Configuration](emulatorjs-config.md)**: operator-level tuning of the EmulatorJS player: per-core settings, control mappings, cache limits, Netplay.
- **[Ruffle Configuration](ruffle-config.md)**: Flash / Shockwave configuration.
- **[Firmware by Platform](firmware-by-platform.md)**: which firmware files each platform needs, file names, and where to get them legally.

## Quick orientation

- **"What platforms does RomM support?"** → [Supported Platforms](supported-platforms.md).
- **"My platform isn't in the list."** → [Custom Platforms](custom-platforms.md) or map it via `system.platforms` in [`config.yml`](../reference/configuration-file.md#systemplatforms).
- **"I want to tweak how an emulator behaves."** → [EmulatorJS Configuration](emulatorjs-config.md).
- **"My game needs a BIOS."** → [Firmware by Platform](firmware-by-platform.md) + [Firmware Management](../administration/firmware-management.md).

## Related sections

- **[In-Browser Play](../using/in-browser-play.md)**: the end-user side of EmulatorJS + Ruffle.
- **[Metadata Providers](../administration/metadata-providers.md)**: which providers each platform has coverage from.
- **[Folder Structure](../getting-started/folder-structure.md)**: how the platform slug maps to on-disk folder names.
