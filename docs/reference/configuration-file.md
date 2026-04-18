---
title: Configuration File
description: Full schema reference for config.yml
---

# Configuration File

RomM reads `config.yml` from `/romm/config/config.yml` inside the container. The whole file is optional: any section you omit falls back to RomM's defaults.

You can edit `config.yml` directly on disk **or** through **Administration → Library Management** in the UI, which is a two-way view of the same file.

Start from the [`config.example.yml`](https://github.com/rommapp/romm/blob/master/examples/config.example.yml) upstream. Two larger fully-worked examples for frontend-integration scenarios:

- [`config.batocera-retrobat.yml`](https://github.com/rommapp/romm/blob/master/examples/config.batocera-retrobat.yml)
- [`config.es-de.example.yml`](https://github.com/rommapp/romm/blob/master/examples/config.es-de.example.yml)

!!! warning "Only set what you need"
    Any omitted section uses the default. Don't copy the full example and then strip sections. Just add what you want to change.

---

## `exclude`

Control what the scanner ignores.

### `exclude.platforms`

Skip entire platform folders. Values are platform slugs, not folder names. See [`system.platforms`](#systemplatforms) if your folders are named differently.

```yaml
exclude:
  platforms: ["ps", "ngc", "gba"]
```

### `exclude.roms.single_file.extensions`

Drop files with these extensions before matching. Applies to files that aren't inside a multi-file folder.

**Default:** `["db", "ini", "tmp", "bak", "lock", "log", "cache", "crdownload"]`

```yaml
exclude:
  roms:
    single_file:
      extensions: ["xml", "txt"]
```

### `exclude.roms.single_file.names`

Unix-glob file-name patterns to skip.

**Default:** `[".DS_Store", ".localized", ".Trashes", ".stfolder", "@SynoResource", "gamelist.xml"]`

```yaml
exclude:
  roms:
    single_file:
      names: ["info.txt", "._*", "*.nfo"]
```

### `exclude.roms.multi_file.names`

Skip whole folders. Used for multi-disc / multi-file games you want invisible.

**Default:** `["@eaDir", "__MACOSX", "$RECYCLE.BIN", ".Trash-*", ".stfolder", ".Spotlight-V100", ".fseventsd", ".DocumentRevisions-V100", "System Volume Information"]`

```yaml
exclude:
  roms:
    multi_file:
      names: ["final fantasy VII", "DLC"]
```

### `exclude.roms.multi_file.parts.names`

Files **inside** a multi-file ROM folder to ignore. Useful for excluding `.nfo`, `._*` macOS attributes, etc. from multi-disc sets.

**Default:** `[".DS_Store", ".localized", ".Trashes", ".stfolder", "@SynoResource", "gamelist.xml"]`

```yaml
exclude:
  roms:
    multi_file:
      parts:
        names: ["data.xml", "._*"]
```

### `exclude.roms.multi_file.parts.extensions`

Extensions to ignore inside a multi-file ROM folder.

**Default:** `["db", "ini", "tmp", "bak", "lock", "log", "cache", "crdownload"]`

```yaml
exclude:
  roms:
    multi_file:
      parts:
        extensions: ["xml", "txt"]
```

---

## `system`

Customise how RomM interprets your filesystem layout.

### `system.platforms`

Map your folder names to RomM platform slugs. Left side = your folder name, right side = canonical slug (see [Supported Platforms](../platforms/supported-platforms.md) for the full list).

```yaml
system:
  platforms:
    gc: "ngc"       # treat "gc/" folder as GameCube
    psx: "ps"       # treat "psx/" folder as PlayStation
    super_nintendo: "snes"
```

### `system.versions`

Associate a platform with its "main" IGDB version. Useful for platforms that have multiple IGDB entries you want collapsed into one (e.g. NAOMI → Arcade).

```yaml
system:
  versions:
    naomi: "arcade"
```

---

## `filesystem`

### `filesystem.roms_folder`

Override the default ROMs folder name (`roms`).

```yaml
filesystem:
  roms_folder: "my_roms"
```

### `filesystem.firmware_folder` _(new in 5.0)_

Override the default BIOS/firmware folder name (`bios`).

```yaml
filesystem:
  firmware_folder: "firmware"
```

### `filesystem.skip_hash_calculation`

Skip hashing on low-power devices. You lose hash-based matching (RetroAchievements, Hasheous, PlayMatch) but scans run much faster.

**Default:** `false`

```yaml
filesystem:
  skip_hash_calculation: true
```

---

## `scan`

### `scan.priority.metadata`

Order metadata providers are queried during a scan. First match wins for descriptive fields (title, description, release date, etc.).

**Default:** `["igdb", "moby", "ss", "ra", "launchbox", "gamelist", "hasheous", "flashpoint", "hltb"]`

```yaml
scan:
  priority:
    metadata:
      - "igdb"
      - "ss"
      - "moby"
```

Values are the provider slugs. Full list:

| Slug | Provider |
| --- | --- |
| `igdb` | IGDB |
| `moby` | MobyGames |
| `ss` | ScreenScraper |
| `ra` | RetroAchievements |
| `launchbox` | LaunchBox |
| `gamelist` | gamelist.xml importer |
| `hasheous` | Hasheous |
| `flashpoint` | Flashpoint |
| `hltb` | HowLongToBeat |
| `tgdb` | TheGamesDB _(5.0)_ |
| `libretro` | Libretro metadata _(5.0)_ |

See [Metadata Providers](../administration/metadata-providers.md) for context on each.

### `scan.priority.artwork`

Same idea, for cover art and screenshots. Defaults to the same order as `scan.priority.metadata` but can differ.

```yaml
scan:
  priority:
    artwork:
      - "ss"        # prefer ScreenScraper artwork
      - "igdb"
      - "moby"
```

### `scan.priority.region` _(enhanced in 5.0)_

Preferred region for titles, cover art, and regional variants. ScreenScraper uses this directly, and other providers respect it where possible.

**Default:** `["us", "wor", "ss", "eu", "jp"]`

```yaml
scan:
  priority:
    region:
      - "us"
      - "eu"
      - "jp"
```

### `scan.priority.language` _(enhanced in 5.0)_

Preferred localisation language.

**Default:** `["en", "fr"]`

```yaml
scan:
  priority:
    language:
      - "en"
      - "es"
      - "fr"
```

### `scan.media`

Which media types to fetch during a scan. Applies primarily to ScreenScraper and the gamelist.xml importer.

| Type | Description |
| --- | --- |
| `box2d` | Normal 2D cover art. Always enabled. |
| `box3d` | 3D box art. |
| `miximage` | Composite image (box + screenshot + logo). |
| `physical` | Physical media (disc, cartridge). |
| `screenshot` | In-game screenshot. Enabled by default. |
| `title_screen` | Title-screen capture. |
| `marquee` | Transparent logo. |
| `fanart` | Community-uploaded fan art. |
| `bezel` | EmulatorJS-compatible bezel. |
| `manual` | PDF manual. Enabled by default. |
| `video` | Gameplay video (big files, watch your disk). |

```yaml
scan:
  media:
    - box2d
    - screenshot
    - manual
    - bezel
```

### `scan.gamelist.export` _(new in 5.0)_

Generate a `gamelist.xml` in each platform folder, compatible with ES-DE / Batocera.

```yaml
scan:
  gamelist:
    export: true
    media:
      thumbnail: box2d
      image: screenshot
```

### `scan.pegasus.export` _(new in 5.0)_

Export metadata in Pegasus-frontend format (`metadata.pegasus.txt`).

```yaml
scan:
  pegasus:
    export: true
```

---

## `emulatorjs`

Configure the in-browser EmulatorJS player.

### `emulatorjs.debug`

Log available EmulatorJS options to the browser console for debugging.

**Default:** `false`

```yaml
emulatorjs:
  debug: true
```

### `emulatorjs.cache_limit`

Per-ROM cache limit in bytes. `null` = unlimited.

```yaml
emulatorjs:
  cache_limit: 52428800   # 50 MB
```

### `emulatorjs.disable_batch_bootup`

DOS-specific. Skips the `autorun.bat` step. Try toggling if DOS games won't boot.

```yaml
emulatorjs:
  disable_batch_bootup: true
```

### `emulatorjs.disable_auto_unload`

By default, EmulatorJS stops the emulator when you leave its page. Disable to keep it running across navigation.

```yaml
emulatorjs:
  disable_auto_unload: true
```

### `emulatorjs.netplay` _(new in 5.0)_

Toggle Netplay and configure STUN/TURN servers. Google's public STUN servers are fine for most setups. Run your own [coturn](https://github.com/coturn/coturn) or use [Metered's free tier](https://www.metered.ca/stun-turn) if you need TURN (symmetric NAT).

```yaml
emulatorjs:
  netplay:
    enabled: true
    ice_servers:
      - urls: "stun:stun.l.google.com:19302"
      - urls: "stun:stun1.l.google.com:19302"
      - urls: "stun:stun2.l.google.com:19302"
      - urls: "turn:openrelay.metered.ca:80"
        username: "openrelayproject"
        credential: "openrelayproject"
      - urls: "turn:openrelay.metered.ca:443"
        username: "openrelayproject"
        credential: "openrelayproject"
```

!!! note "Nightly CDN caveat"
    With Netplay enabled, EmulatorJS loads some assets (localisations included) from its nightly CDN (`https://cdn.emulatorjs.org/nightly/...`). Occasional 404s or untranslated strings can appear when the nightly has a transient mismatch. Usually self-heals by the next RomM image update.

### `emulatorjs.settings`

Per-core emulator options. Use `default` to apply to every core.

```yaml
emulatorjs:
  settings:
    parallel_n64:
      vsync: disable
    snes9x:
      snes9x_region: ntsc
    default:
      fps: show
```

Core names must match the EmulatorJS core identifier exactly. See the `getSupportedEJSCores` utility in the frontend source for the full list, or leave the core out and use `default`.

### `emulatorjs.controls`

Map keyboard and controller buttons per core, per player.

```yaml
emulatorjs:
  controls:
    snes9x:
      0:                       # player 1
        0:                     # button slot
          value: x             # keyboard key
          value2: BUTTON_2     # controller button
      1:                       # player 2
        0:
          value: /
          value2: BUTTON_2
```

See the [EmulatorJS control-mapping docs](https://emulatorjs.org/docs4devs/control-mapping/) for the button-slot reference.

---

## Editing via the UI

Everything above is also available from the Library Management page in the web UI, and edits there write back to the same `config.yml`. Either path works. They're not separate stores.

## Per-file alternatives

RomM also ships two pre-built config.yml variants for people coming from existing frontends. Copy them wholesale rather than writing one from scratch:

- [`config.batocera-retrobat.yml`](https://github.com/rommapp/romm/blob/master/examples/config.batocera-retrobat.yml): Batocera / RetroBat layouts.
- [`config.es-de.example.yml`](https://github.com/rommapp/romm/blob/master/examples/config.es-de.example.yml): ES-DE layout.

## Related

- [Folder Structure](../getting-started/folder-structure.md): how the filesystem shape interacts with `config.yml`.
- [Metadata Providers](../administration/metadata-providers.md): per-provider detail for the `scan.priority.*` slugs.
- [Scanning & Watcher](../administration/scanning-and-watcher.md): how `exclude.*` interacts with scan runs.
- [Environment Variables](environment-variables.md): env-var overrides for some of the same knobs.
