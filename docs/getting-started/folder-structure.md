---
title: Folder Structure
description: How to organise your library on disk
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Folder Structure

RomM expects your library to be organised in one of two layouts. **Structure A** is what it scans unless told otherwise. **Structure B** is not auto-detected, so a library laid out that way has to declare it as a [structure template](#custom-library-structure) in `config.yml`, and RomM refuses to start with the two lines you need if it spots that layout undeclared.

## The two layouts

Both layouts separate ROMs from BIOS files, and they differ on whether the split lives at the top of the tree or inside each platform.

- **Structure A (recommended)**: one top-level `roms/`, one top-level `bios/`, platforms nested inside each

```text
/roms/{platform}/
/bios/{platform}/
```

- **Structure B (opt-in)**: one folder per platform at the top, `roms/` and `bios/` inside each

```text
/{platform}/roms/
/{platform}/bios/
```

Structure B is declared with two templates, and the [custom library structure](#custom-library-structure) section below covers the syntax:

```yaml
filesystem:
    structure:
        default: "{platform}/roms/{game}"
        firmware: "{platform}/bios"
```

As the BIOS/firmware tree is **optional**, only platforms that require firmware for emulation need it.

### Mount point

The path you mount into the container as `/romm/library` depends on which structure you pick:

- **Structure A**: mount the parent of the `roms/` folder.
- **Structure B**: mount the parent of the platform folders.

See the [reference Docker Compose](quick-start.md) for where `/romm/library` lives.

<!-- prettier-ignore -->
!!! tip "Platform folder names"
    The platform folder name should match a slug from the full list in [Supported Platforms](../platforms/supported-platforms.md), matched case-insensitively so `SNES/` and `snes/` are the same platform. RomM also recognises the folder names Batocera, RetroBat and ES-DE use, so a library that already reads `megadrive/`, `gamecube/` or `n3ds/` scans as-is (see [Folder name aliases](../platforms/supported-platforms.md#folder-name-aliases)). For anything else (say, `super_nintendo/` instead of `snes/`), bind the folder yourself via [`system.platforms`](../reference/configuration-file.md#systemplatforms) in `config.yml`.

## Multi-file games

Some games come as **folders** instead of single files, holding multiple discs, DLC, manuals, or patches alongside the game itself. These sub-folder names are recognised and surfaced as tags in the UI, in singular or plural form:

| Folder           | Holds                                               |
| ---------------- | --------------------------------------------------- |
| `dlc`            | Downloadable content                                |
| `update`         | Game updates                                        |
| `patch`          | [Patch files](../using/rom-patcher.md)              |
| `hack`, `mod`    | Community modifications                             |
| `translation`    | Fan translations                                    |
| `demo`           | Demo builds                                         |
| `prototype`      | Prototype builds                                    |
| `manual` \*      | Manuals                                             |
| `walkthrough` \* | [Walkthroughs](../using/walkthroughs.md)            |
| `soundtrack` \*  | Audio tracks for the [Jukebox](../using/jukebox.md) |
| `cheat` \*       | Cheat files                                         |
| `screenshot` \*  | Screenshots                                         |

\* These never contain a ROM binary, so hashing and title-id extraction skip them.

## Visual reference

<table>
<tr>
    <th style="text-align: center"><b>Structure A (recommended)</b></th>
    <th style="text-align: center"><b>Structure B (opt-in)</b></th>
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
        │  │     ├─ prototype
        │  │     ├─ walkthrough
        │  │     ├─ soundtrack
        │  │     ├─ cheat
        │  │     └─ screenshot
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
        │  │     ├─ prototype
        │  │     ├─ walkthrough
        │  │     ├─ soundtrack
        │  │     ├─ cheat
        │  │     └─ screenshot
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

## Custom library structure

Both layouts above are **structure templates**, and so is anything deeper. `filesystem.structure` in [`config.yml`](../reference/configuration-file.md#filesystemstructure) holds them: `default` is the library-wide ROM layout (`roms/{platform}/{game}` unless you say otherwise), `firmware` is the firmware one (`bios/{platform}`), and any other key overrides the ROM layout for one platform.

### Syntax

A template is a `/`-separated path relative to the **library root**, the folder you mount as `/romm/library`. A bare section is a literal folder name, matched exactly, and a section wrapped in braces is a macro.

- `{platform}` marks the platform folder, and every section before it has to be a literal so there is one known folder to enumerate platforms in. A per-platform override may spell that folder out by name instead, which is how its key already reads (`roms/ps3/{category}/{game}` under the `ps3` key).
- `{game}` is the **terminal** and has to be the last section. It marks the level where a game begins, and at that level a file is a game of its own while a folder is one multi-file game, so multi-disc and `cue`+`bin` games stay whole without you declaring anything.
- Any other braced section (`{region}`, `{category}`, or whatever you want to call it) is a wildcard directory level: it matches any folder name and is purely organisational.
- `{library}` is rejected, because a template is already relative to the library root.

```yaml
filesystem:
    structure:
        # The defaults, spelled out
        default: "roms/{platform}/{game}"
        firmware: "bios/{platform}"
        # roms/snes/USA/foo.sfc, roms/snes/Japan/bar.sfc
        snes: "roms/{platform}/{region}/{game}"
        # roms/ps3/Disc/Game/, roms/ps3/PSN/Game/ -> each folder is one game
        ps3: "roms/{platform}/{category}/{game}"
```

Platform keys are matched case-insensitively, like `system.platforms`, so `Atari - 2600` and `atari - 2600` name the same platform. `default` and `firmware` are reserved, and a platform folder named either is read as the layout key rather than as an override.

The `firmware` template takes only literal folder names around `{platform}`, no wildcard levels and no `{game}`, because it points at a folder rather than at a set of games.

Every per-platform override has to agree with `default` on where the platform folder itself sits, since platform discovery enumerates a single folder. Pairing `default: "roms/{platform}/{game}"` with `snes: "games/{platform}/{game}"` is refused at startup.

### Several templates for one platform

A platform can declare a **list** of templates, and discovery is their union. That covers the mixed layout no single fixed-depth template can express: loose games directly in the platform folder **and** games inside grouping subfolders below it.

```yaml
filesystem:
    structure:
        nes:
            - "roms/{platform}/{game}" # roms/nes/game01.nes
            - "roms/{platform}/{category}/{game}" # roms/nes/Hacks/game03.nes
```

### Moving games around

Game identity is content-based, so a template isn't a cage: move or rename a game within it and the next scan recognises it by its hashes and relocates the existing entry in place, so its saves, states, play history, favourites and collection membership follow it. Removing a platform's override moves nothing on disk: the platform falls back to `structure.default`, so the games that no longer sit where that template expects them are flagged as missing from the filesystem, and the folders that used to group them are picked up as multi-file games instead. Flatten the library out yourself and the next scan matches each game by hash and relocates it rather than importing a duplicate.

<!-- prettier-ignore -->
!!! warning "Relocation needs an identity"
    Matching a moved file to its entry needs all three of its hashes (CRC, MD5, SHA-1), so hashing has to be on (see [`filesystem.skip_hash_calculation`](../reference/configuration-file.md#filesystemskip_hash_calculation)). Platforms RomM doesn't hash (Switch, PS3, PS4, the PC and mobile platforms) fall back to the Title ID read out of the binary. With neither available, or when two entries missing from the same platform share an identity, the file is imported as a new game and the old entry stays flagged as missing from the filesystem.

### Notes

- Hidden (dot-prefixed) folders are never descended into or surfaced.
- A folder a template descends into is a grouping level, not a game. With `roms/{platform}/{game}` and `roms/{platform}/{category}/{game}` declared together, a folder holding discovered games is a category, and only folders no template descends into stay multi-file games.
- A folder previously scanned as one multi-file game that a new template descends into leaves its old entry marked as missing from the filesystem (the scan log flags it). Delete the stale entry to clean up.
- Uploading through the web UI needs a folder RomM can derive, so a platform whose every template carries a wildcard level rejects uploads. Add those files from the filesystem and rescan the platform.
- Two files with the same name in different folders become distinct games. A `gamelist.xml` entry is matched to one of them by its `<path>` relative to the platform folder, and an entry carrying only a bare file name still matches as long as a single game has that name.
- Exported metadata follows the structure too: `gamelist.xml` and `metadata.pegasus.txt` entries carry each game's path relative to the platform folder, and exported media mirrors those folders.

## Naming convention

Filenames are parsed for region, language, revision, and arbitrary tags, with both `[]` and `()` delimiters supported:

- **Region/language**: both ISO-like codes and full names. Add a custom region or language by prefixing with `reg`/`reg-` (e.g. `reg MyOwnLang` or `reg-MyOwnLang`).
- **Revision**: prefix with `rev`/`rev-` (e.g. `rev v1`, `rev-1`)
- **Arbitrary tags**: anything else in brackets is imported verbatim (e.g. `tetris [1.0001](HACK)[!].gba`)

Inline tags like `(igdb-1234)` in filenames can be used to force a match to a specific provider entry, covered in [Metadata Providers → Filename tags](metadata-providers.md#metadata-tags-in-filenames).

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
