---
title: Supported Platforms
description: Every supported platform with metadata provider coverage
---

# Supported Platforms

RomM ships support for ~400 platforms. "Support" means:

1. **RomM recognises the folder name** and maps it to a canonical platform.
2. **At least one metadata provider** has coverage.
3. **EmulatorJS** may have a playable core (flagged per platform in the table below).

Name your folder after the **platform slug** in the table, or after one of the [folder name aliases](#folder-name-aliases) below. Anything else needs a [`system.platforms`](../reference/configuration-file.md#systemplatforms) binding in `config.yml` (see [Folder Structure](../getting-started/folder-structure.md)).

## Platform slugs + coverage

--8<-- "supported-platforms.md"

## What the columns mean

- **Slug**: the folder name RomM expects. Matches the IGDB platform slug where possible. Matched case-insensitively, so `SNES/` and `snes/` are the same platform.
- **Name**: the human-readable platform name
- **Providers**: which metadata providers have at least partial coverage (see [Metadata Providers](../getting-started/metadata-providers.md)).
- **EmulatorJS**: a playable in-browser core exists (see [Configuration File → `emulatorjs`](../reference/configuration-file.md#emulatorjs) for server owner-level tuning).
- **Firmware**: platform needs BIOS files for emulation (see [Firmware Management](../administration/firmware-management.md)).

## Folder name aliases

Batocera, RetroBat and ES-DE name a fair number of their system folders differently from RomM. Those names are recognised out of the box, so a library laid out for one of those frontends scans without a `system.platforms` binding for every platform.

--8<-- "platform-aliases.md"

Aliases are the last thing RomM tries, so a `system.platforms` binding always overrides one. See [`system.platforms`](../reference/configuration-file.md#systemplatforms) for the full order.

Note that aliases are not one-to-one. All four Amiga models land on `amiga` and every arcade board lands on `arcade`, so those games end up sharing a platform. And a folder name that is itself a slug is matched before the aliases are reached, which means a frontend using that name for something broader still needs a binding: `atari800/` holds the whole Atari 8-bit family in ES-DE and Batocera, while RomM reads `atari800` as the Atari 800 alone. The example configs for both frontends bind it to `atari8bit`.

If the folder name you want is missing, open an issue at [rommapp/romm](https://github.com/rommapp/romm/issues) so it can be added for everyone, and bind it in `config.yml` meanwhile.

## Platform not listed?

Two options:

- **[Custom Platforms](custom-platforms.md)**: add an unknown platform. RomM will recognise the folder but won't have metadata or emulator support.
- **Map to an existing slug** via `config.yml` if yours is a naming variant of something RomM already supports (e.g. `super_nintendo` → `snes`).

Open an issue at [rommapp/romm](https://github.com/rommapp/romm/issues) if you believe a platform should be added to the built-in list.

## Where the tables come from

Both tables on this page are generated against the upstream registry at the ref pinned in [`scripts/sources.toml`](https://github.com/rommapp/docs/blob/main/scripts/sources.toml), and the release-bump workflow regenerates them whenever that pin moves. Regenerate locally with:

```sh
uv run python -m scripts.gen_platforms         # the platform table
uv run python -m scripts.gen_platform_aliases  # the folder-alias table
```

The platform table comes from romm's own generator, so `gen_platforms` needs a romm checkout (`ROMM_SRC`). The alias table is parsed straight out of [`platform_aliases.py`](https://github.com/rommapp/romm/blob/master/backend/utils/platform_aliases.py) and needs no checkout.

## See also

- [Folder Structure](../getting-started/folder-structure.md): how platform slugs map to on-disk folders
- [Custom Platforms](custom-platforms.md): adding platforms outside the built-in list
- [Metadata Providers](../getting-started/metadata-providers.md): provider coverage deep-dive
- [In-Browser Play → EmulatorJS](../using/in-browser-play/emulatorjs.md): EmulatorJS core catalogue
- [Firmware Management](../administration/firmware-management.md): how RomM stores and serves BIOS files
