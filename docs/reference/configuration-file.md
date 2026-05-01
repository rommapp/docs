---
title: Configuration File
description: Full schema reference for config.yml
---

# Configuration File

RomM reads `config.yml` from `/romm/config/config.yml` inside the container. The whole file is optional: any section you omit falls back to the defaults. You can edit `config.yml` directly on disk **or** through **Administration → Library Management** in the UI, which is a two-way view of the same file.

Start from the [`config.example.yml`](https://github.com/rommapp/romm/blob/master/examples/config.example.yml) upstream. Two larger fully-worked examples for frontend-integration scenarios:

- [`config.batocera-retrobat.yml`](https://github.com/rommapp/romm/blob/master/examples/config.batocera-retrobat.yml)
- [`config.es-de.example.yml`](https://github.com/rommapp/romm/blob/master/examples/config.es-de.example.yml)

<!-- prettier-ignore -->
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

Files **inside** a multi-file ROM folder to ignore (e.g. `.nfo`, `._*` macOS attributes, similar noise from multi-disc sets).

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

Customise how your filesystem layout is interpreted, and how platforms are identified.

### `system.platforms`

Map your folder names to [supported platform](../platforms/supported-platforms.md) slugs.

```yaml
system:
    platforms:
        gc: "ngc" # treat "gc/" folder as GameCube
        psx: "ps" # treat "psx/" folder as PlayStation
        super_nintendo: "snes"
```

### `system.versions`

Associate a platform with its "main" IGDB version, for platforms that have multiple IGDB entries you want collapsed into one (e.g. NAOMI → Arcade).

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

### `filesystem.firmware_folder`

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

| Slug         | Provider              |
| ------------ | --------------------- |
| `igdb`       | IGDB                  |
| `moby`       | MobyGames             |
| `ss`         | ScreenScraper         |
| `ra`         | RetroAchievements     |
| `launchbox`  | LaunchBox             |
| `gamelist`   | gamelist.xml importer |
| `hasheous`   | Hasheous              |
| `flashpoint` | Flashpoint            |
| `hltb`       | HowLongToBeat         |
| `tgdb`       | TheGamesDB            |
| `libretro`   | Libretro metadata     |

See [Metadata Providers](../administration/metadata-providers.md) for context on each.

### `scan.priority.artwork`

Same idea, for cover art and screenshots. Defaults to the same order as `scan.priority.metadata` but can differ.

```yaml
scan:
    priority:
        artwork:
            - "ss" # prefer ScreenScraper artwork
            - "igdb"
            - "moby"
```

### `scan.priority.region`

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

### `scan.priority.language`

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

| Type           | Description                                  |
| -------------- | -------------------------------------------- |
| `box2d`        | Normal 2D cover art. Always enabled.         |
| `box3d`        | 3D box art.                                  |
| `miximage`     | Composite image (box + screenshot + logo).   |
| `physical`     | Physical media (disc, cartridge).            |
| `screenshot`   | In-game screenshot. Enabled by default.      |
| `title_screen` | Title-screen capture.                        |
| `marquee`      | Transparent logo.                            |
| `fanart`       | Community-uploaded fan art.                  |
| `bezel`        | EmulatorJS-compatible bezel.                 |
| `manual`       | PDF manual. Enabled by default.              |
| `video`        | Gameplay video (big files, watch your disk). |

```yaml
scan:
    media:
        - box2d
        - screenshot
        - manual
        - bezel
```

### `scan.gamelist.export`

Generate a `gamelist.xml` in each platform folder, compatible with ES-DE / Batocera.

```yaml
scan:
    gamelist:
        export: true
        media:
            thumbnail: box2d
            image: screenshot
```

### `scan.pegasus.export`

Export metadata in Pegasus-frontend format (`metadata.pegasus.txt`).

```yaml
scan:
    pegasus:
        export: true
```

---

## `emulatorjs`

These keys tune the in-browser EmulatorJS player for every user on your instance. The end-user side lives in [In-Browser Play → EmulatorJS](../using/in-browser-play/emulatorjs.md). To disable EmulatorJS altogether (on the slim image, or when running headless with companion apps), set `DISABLE_EMULATOR_JS=true` in your env vars.

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
    cache_limit: 52428800 # 50 MB
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

### `emulatorjs.netplay`

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

<!-- prettier-ignore -->
!!! note "Nightly CDN caveat"
    With Netplay enabled, EmulatorJS loads some assets (localisations included) from its nightly CDN (`https://cdn.emulatorjs.org/nightly/...`). Occasional 404s or untranslated strings can appear when the nightly has a transient mismatch, which usually self-heals by the next image update.

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

Core names must match the EmulatorJS core identifier exactly. To discover core names and per-core option keys, turn on `debug: true`, load a game in that core, open the browser console, filter for "option", and copy the keys you care about. Upstream reference is available in [EmulatorJS core options](https://emulatorjs.org/docs4devs/settings/).

### `emulatorjs.controls`

Map keyboard and controller buttons per core, per player.

```yaml
emulatorjs:
    controls:
        snes9x:
            0: # player 1
                0: # button slot
                    value: x # keyboard key
                    value2: BUTTON_2 # controller button
            1: # player 2
                0:
                    value: /
                    value2: BUTTON_2
```

See the [EmulatorJS control-mapping docs](https://emulatorjs.org/docs4devs/control-mapping/) for the button-slot reference. Users can override these defaults in-game via Menu → **Controls**, the config.yml setting only sets the starting point.

#### Worked example: 2-player SNES

```yaml
emulatorjs:
    settings:
        snes9x:
            snes9x_region: ntsc
    controls:
        snes9x:
            0: # P1 on keyboard (WASD cluster)
                0: { value: ",", value2: "BUTTON_2" } # B
                1: { value: ".", value2: "BUTTON_3" } # A
                2: { value: "l", value2: "BUTTON_1" } # Y
                3: { value: "p", value2: "BUTTON_4" } # X
            1: # P2 on arrows + numpad
                0: { value: "/", value2: "BUTTON_2" }
                1: { value: "'", value2: "BUTTON_3" }
```

### Operator-level vs per-user

Most settings under `emulatorjs.settings` and `emulatorjs.controls` can be overridden by users in-game (Menu → Settings, Menu → Controls). Per-user values take precedence, the config.yml setting is the fallback.

| Where the setting lives           | Who it affects       | Survives upgrades? |
| --------------------------------- | -------------------- | ------------------ |
| Operator: `config.yml` / env vars | Everyone, as default | Yes                |
| Per-user: in-game Menu → Settings | Just that user       | Yes                |
| Per-user: in-game Menu → Controls | Just that user       | Yes                |

---

## Related

- [Folder Structure](../getting-started/folder-structure.md): how the filesystem shape interacts with `config.yml`
- [Metadata Providers](../administration/metadata-providers.md): per-provider detail for the `scan.priority.*` slugs
