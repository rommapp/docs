---
title: Folder Structure
description: How to organise your library on disk
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Folder Structure

RomM expects your library to be organised in one of two layouts. It tries **Structure A** first, and falls back to **Structure B** if A isn't found. This auto-detection is per-library (not per-platform), so you don't pick one up front. Just arrange files the way you prefer, and it'll figure it out.

## The two layouts

Both layouts separate ROMs from BIOS files, and they differ on whether the split lives at the top of the tree or inside each platform.

- **Structure A (recommended)**: one top-level `roms/`, one top-level `bios/`, platforms nested inside each

```text
/roms/{platform}/
/bios/{platform}/
```

- **Structure B (fallback)**: one folder per platform at the top, `roms/` and `bios/` inside each

```text
/{platform}/roms/
/{platform}/bios/
```

As the BIOS/firmware tree is **optional**, only platforms that require firmware for emulation need it.

### Mount point

The path you mount into the container as `/romm/library` depends on which structure you pick:

- **Structure A**: mount the parent of the `roms/` folder.
- **Structure B**: mount the parent of the platform folders.

See the [reference Docker Compose](quick-start.md) for where `/romm/library` lives.

<!-- prettier-ignore -->
!!! tip "Platform folder names"
    The platform folder name has to match a known slug from the full list in [Supported Platforms](../platforms/supported-platforms.md). If your existing folder names don't match (say, `super_nintendo/` instead of `snes/`), override the mapping via `system.platforms` in [`config.yml`](../reference/configuration-file.md).

## Multi-file games

Some games come as **folders** instead of single files, which could include multiple disc, DLCs, manuals, or patches. These sub-folder names are recognised and surfaced as tags in the UI: `dlc`, `hack`, `manual`, `mod`, `patch`, `update`, `demo`, `translation`, `prototype`.

## Visual reference

<table>
<tr>
    <th style="text-align: center"><b>Structure A (recommended)</b></th>
    <th style="text-align: center"><b>Structure B (fallback)</b></th>
</tr>
<tr>
    <td style="text-align: center">
        <code>library/roms/{platform}/{game}</code>
    </td>
    <td style="text-align: center">
        <code>library/{platform}/roms/{game}</code>
    </td>
</tr>
<tr>
    <td>
        <pre style="font-size: 0.85em;">
        library/
        ├─ roms/
        │  ├─ gbc/
        │  │  ├─ game_1.gbc
        │  │  └─ game_2.gbc
        │  │
        │  ├─ gba/
        │  │  ├─ game_3.gba
        │  │  └─ game_4/
        │  │     ├─ game_4.gba
        │  │     ├─ dlc
        │  │     │  ├─ game_4_dlc_1.7z
        │  │     │  └─ game_4_dlc_2.7z
        │  │     ├─ hack
        │  │     │  └─ game_4_hardmode.rar
        │  │     ├─ manual
        │  │     │  └─ game_4_manual.pdf
        │  │     ├─ mod
        │  │     │  └─ game_4_crazy_mode.zip
        │  │     ├─ patch
        │  │     │  └─ game_4_patch_v1.1.zip
        │  │     ├─ update
        │  │     ├─ demo
        │  │     ├─ translation
        │  │     └─ prototype
        │  │
        │  └─ ps/
        │     ├─ game_5/
        │     │   ├─ game_5_cd_1.iso
        │     │   └─ game_5_cd_2.iso
        │     │
        │     └─ game_6.iso
        │
        └─ bios/
           ├─ gba/
           │  └─ gba_bios.bin
           │
           └─ ps/
              ├─ scph1001.bin
              ├─ scph5501.bin
              └─ scph5502.bin
        </pre>
    </td>
    <td>
        <pre style="font-size: 0.85em;">
        library/
        ├─ gbc/
        │  └─ roms/
        │     ├─ game_1.gbc
        │     └─ game_2.gbc
        │
        ├─ gba/
        │  ├─ roms/
        │  │  ├─ game_3.gba
        │  │  └─ game_4/
        │  │     ├─ game_4.gba
        │  │     ├─ dlc
        │  │     ├─ hack
        │  │     ├─ manual
        │  │     ├─ mod
        │  │     ├─ patch
        │  │     ├─ update
        │  │     ├─ demo
        │  │     ├─ translation
        │  │     └─ prototype
        │  │
        │  └─ bios/
        │     └─ gba_bios.bin
        │
        └─ ps/
           ├─ roms/
           │  ├─ game_5/
           │  │  ├─ game_5_cd_1.iso
           │  │  └─ game_5_cd_2.iso
           │  │
           │  └─ game_6.iso
           │
           └─ bios/
              ├─ scph1001.bin
              ├─ scph5501.bin
              └─ scph5502.bin
        </pre>
    </td>
</tr>
</table>

<!-- prettier-ignore -->
!!! note "Starting from scratch?"
    If you upload files through the web UI without any existing structure, it'll create **Structure A** on your behalf.

## Naming convention

Filenames are parsed for region, language, revision, and arbitrary tags, with both `[]` and `()` delimiters supported:

- **Region/language**: both ISO-like codes and full names. Add a custom region or language by prefixing with `reg`/`reg-` (e.g. `reg MyOwnLang` or `reg-MyOwnLang`).
- **Revision**: prefix with `rev`/`rev-` (e.g. `rev v1`, `rev-1`)
- **Arbitrary tags**: anything else in brackets is imported verbatim (e.g. `tetris [1.0001](HACK)[!].gba`)

Inline tags like `(igdb-1234)` in filenames can be used to force a match to a specific provider entry, covered in [Metadata Providers → Filename tags](../administration/metadata-providers.md#metadata-tags-in-filenames).

<div class="grid cards" markdown>

<div markdown>

### Supported languages

| Code   | Language    |
| ------ | ----------- |
| Ar     | Arabic      |
| Da     | Danish      |
| De     | German      |
| El     | Greek       |
| En     | English     |
| Es     | Spanish     |
| Fi     | Finnish     |
| Fr     | French      |
| It     | Italian     |
| Ja     | Japanese    |
| Ko     | Korean      |
| Nl     | Dutch       |
| No     | Norwegian   |
| Pl     | Polish      |
| Pt     | Portuguese  |
| Ru     | Russian     |
| Sr     | Serbian     |
| Sv     | Swedish     |
| Zh     | Chinese     |
| nolang | No Language |

</div>

<div markdown>

### Supported regions

| Code | Region        |
| ---- | ------------- |
| A    | Australia     |
| AS   | Asia          |
| B    | Brazil        |
| C    | Canada        |
| CH   | China         |
| E    | Europe        |
| F    | France        |
| FN   | Finland       |
| G    | Germany       |
| GR   | Greece        |
| H    | Holland       |
| HK   | Hong Kong     |
| I    | Italy         |
| J    | Japan         |
| K    | Korea         |
| NL   | Netherlands   |
| NO   | Norway        |
| PD   | Public Domain |
| R    | Russia        |
| S    | Spain         |
| SW   | Sweden        |
| T    | Taiwan        |
| U    | USA           |
| UK   | England       |
| UNK  | Unknown       |
| UNL  | Unlicensed    |
| W    | World         |

</div>

</div>
