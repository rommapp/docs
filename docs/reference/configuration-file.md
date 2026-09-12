---
title: Configuration File
description: Full schema reference for config.yml
---

# Configuration File

RomM reads `config.yml` from `/romm/config/config.yml` inside the container. The whole file is optional: any section you omit falls back to the defaults. You can edit `config.yml` directly on disk **or** through **Library → Library Management** in the settings dropdown, which is a two-way view of the same file.

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

Skip entire platform folders. Values are platform slugs, not folder names (see [`system.platforms`](#systemplatforms) if your folders are named differently).

```yaml
exclude:
    platforms: ["ps", "ngc", "gba"]
```

### `exclude.roms.single_file.extensions`

Drop files with these extensions before matching, only for files that aren't inside a multi-file folder.

**Default:** `["db", "tmp", "bak", "lock", "log", "cache", "crdownload", "assembling"]`

```yaml
exclude:
    roms:
        single_file:
            extensions: ["xml", "txt"]
```

### `exclude.roms.single_file.names`

Unix-glob file-name patterns to skip.

**Default:** `[".DS_Store", ".localized", ".Trashes", ".stfolder", "@SynoResource", "*:Zone.Identifier", "gamelist.xml", "metadata.pegasus.txt"]`

```yaml
exclude:
    roms:
        single_file:
            names: ["info.txt", "._*", "*.nfo"]
```

### `exclude.roms.multi_file.names`

Skip whole folders. Used for multi-disc/multi-file games you want invisible.

The default already covers the system folders that are never a platform, plus every per-media-type folder ES-DE, Batocera and the [Pegasus export](exports.md) drop beside your ROMs (`covers`, `screenshots`, `manuals` and the rest). Your list gets added to that rather than replacing it.

```yaml
exclude:
    roms:
        multi_file:
            names: ["final fantasy VII", "DLC"]
```

### `exclude.roms.multi_file.parts.names`

Files **inside** a multi-file ROM folder to ignore (e.g. `.nfo`, `._*` macOS attributes, similar noise from multi-disc sets).

**Default:** the same list as [`exclude.roms.single_file.names`](#excluderomssingle_filenames)

```yaml
exclude:
    roms:
        multi_file:
            parts:
                names: ["data.xml", "._*"]
```

### `exclude.roms.multi_file.parts.extensions`

Extensions to ignore inside a multi-file ROM folder.

**Default:** the same list as [`exclude.roms.single_file.extensions`](#excluderomssingle_fileextensions)

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

Map your folder names to [supported platform](../platforms/supported-platforms.md) slugs, for folders RomM doesn't recognise or gets wrong.

```yaml
system:
    platforms:
        super_nintendo: "snes" # treat "super_nintendo/" folder as SNES
        my_saturn_dump: "saturn"
```

Keys are folder names, values are platform slugs, and both are matched case-insensitively, so `GameCube: "ngc"` and `gamecube: "ngc"` do the same thing.

RomM tries a folder name against each of these in turn and takes the first hit:

1. A `system.platforms` or [`system.versions`](#systemversions) binding.
2. The folder name itself, if it already is a platform slug.
3. The [built-in folder aliases](../platforms/supported-platforms.md#folder-name-aliases) for names Batocera, RetroBat and ES-DE use (`megadrive/`, `gamecube/`, `n3ds/`, `mame/`, ...).

A name that matches none of them becomes a [custom platform](../platforms/custom-platforms.md), with no metadata coverage.

A binding beats an alias, so `mame: "mame"` gets you a separate Mame platform instead of folding that folder into Arcade.

A folder name that is itself a slug never gets as far as the aliases, which bites when a frontend uses the name for something broader. ES-DE and Batocera put the whole Atari 8-bit family in `atari800/`, while RomM reads `atari800` as the Atari 800 alone, so that one needs `atari800: "atari8bit"` written out. The shipped Batocera and ES-DE configs both include it.

### `system.versions`

Associate a platform with its "main" IGDB version, for platforms that have multiple IGDB entries you want collapsed into one (e.g. NAOMI → Arcade).

```yaml
system:
    versions:
        naomi: "arcade"
```

---

## `filesystem`

### `filesystem.structure`

Describe the whole library layout. A template is a `/`-separated path relative to the library root, where `{platform}` marks the platform folder and `{game}` the level a game begins at (a file there is one game, a folder one multi-file game). Any other braced section is a wildcard level matching any folder name.

- `default` is the library-wide ROM layout, `roms/{platform}/{game}` if unset.
- `firmware` is the firmware layout, `bios/{platform}` if unset, and it takes only literal folder names around `{platform}`.
- Any other key is a platform folder name (matched case-insensitively, like `system.platforms`) overriding the ROM layout for that platform, as one template or a list of them whose discovery is unioned. An override has to agree with `default` on where the platform folder sits.

```yaml
filesystem:
    structure:
        default: "roms/{platform}/{game}"
        firmware: "bios/{platform}"
        snes: "roms/{platform}/{region}/{game}"
        ps3: "roms/{platform}/{category}/{game}"
        nes:
            - "roms/{platform}/{game}"
            - "roms/{platform}/{category}/{game}"
```

See [Folder Structure → Custom library structure](../getting-started/folder-structure.md#custom-library-structure) for the full syntax and how moving games between folders is handled.

<!-- prettier-ignore -->
!!! warning "`roms_folder` and `firmware_folder` were retired"
    Each named one path segment that a template now spells out, so RomM refuses to start while either is set, printing the template that reproduces the layout. `roms_folder: "my_roms"` becomes `default: "my_roms/{platform}/{game}"`, and `firmware_folder: "firmware"` becomes `firmware: "firmware/{platform}"`.

### `filesystem.skip_hash_calculation`

Skip hashing on low-power devices. You lose hash-based matching (RetroAchievements, Hasheous, PlayMatch) but scans run much faster.

**Default:** `false`

```yaml
filesystem:
    skip_hash_calculation: true
```

### `filesystem.skip_title_id_extraction`

Skip reading the platform-native Title ID out of ROM binaries. That ID is what identifies a game on non-hashed platforms, and it records where the game writes its saves, so expect worse matching on those platforms with this on. See [Title ids read from the binary](../administration/scanning-and-watcher.md#title-ids-read-from-the-binary) for which platforms have one and what the ID carries.

**Default:** `false`

```yaml
filesystem:
    skip_title_id_extraction: true
```

### `filesystem.embed_switch_title_ids`

Rename Switch ROMs on disk so their filename ends in `[TITLEID][vVERSION]`, which is what most Switch tooling expects to see. Disabled by default because it rewrites file names.

**Default:** `false`

```yaml
filesystem:
    embed_switch_title_ids: true
```

---

## `scan`

### `scan.priority.metadata`

Order metadata providers are queried during a scan. First match wins for descriptive fields (title, description, release date, etc.).

**Default:** `["igdb", "moby", "ss", "ra", "launchbox", "gamelist", "hasheous", "tgdb", "flashpoint", "steam", "hltb", "demozoo", "pouet", "csdb"]`

```yaml
scan:
    priority:
        metadata:
            - "igdb"
            - "ss"
            - "moby"
```

Values are the provider slugs. Full list:

| Slug         | Provider                        |
| ------------ | ------------------------------- |
| `igdb`       | IGDB                            |
| `moby`       | MobyGames                       |
| `ss`         | ScreenScraper                   |
| `ra`         | RetroAchievements               |
| `launchbox`  | LaunchBox                       |
| `gamelist`   | gamelist.xml importer           |
| `hasheous`   | Hasheous                        |
| `playmatch`  | Playmatch                       |
| `flashpoint` | Flashpoint                      |
| `steam`      | Steam, on the PC platforms only |
| `hltb`       | HowLongToBeat                   |
| `demozoo`    | Demozoo, demoscene productions  |
| `pouet`      | Pouët, demoscene productions    |
| `csdb`       | CSDb, C64 demoscene productions |
| `tgdb`       | TheGamesDB                      |
| `sgdb`       | SteamGridDB, artwork only       |
| `libretro`   | Libretro metadata, artwork only |

See [Metadata Providers](../getting-started/metadata-providers.md) for context on each.

### `scan.priority.artwork`

Same idea but for cover art and screenshots, with a default of its own: `["sgdb", "igdb", "moby", "ss", "libretro", "ra", "launchbox", "gamelist", "hasheous", "tgdb", "flashpoint", "steam", "hltb", "demozoo", "pouet", "csdb"]`.

```yaml
scan:
    priority:
        artwork:
            - "ss" # prefer ScreenScraper artwork
            - "igdb"
            - "moby"
```

### `scan.priority.cover`, `scan.priority.screenshot`, `scan.priority.manual`

Optional per-field overrides that let you prioritise sources differently for each artwork type. Any field you omit falls back to the shared [`scan.priority.artwork`](#scanpriorityartwork) order, so only set the ones you want to diverge.

```yaml
scan:
    priority:
        cover: # Cover art only
            - "igdb"
            - "ss"
        screenshot: # Screenshots only
            - "ss"
            - "igdb"
        manual: # Game manuals only
            - "launchbox"
```

### `scan.priority.region`

Preferred region for titles, cover art, and regional variants. ScreenScraper uses this directly, and other providers respect it where possible.

This also decides which dump the gallery shows when you own several copies of a game. Siblings collapse into one card, and the winner is whichever region sits highest in this list, with pre-release dumps pushed below full releases. Regions you haven't listed come last, so a Japan-only release still wins when it's the only one there.

**Default:** `["us", "wor", "ss", "eu", "jp"]`

```yaml
scan:
    priority:
        region:
            - "us"
            - "eu"
            - "jp"
```

### `scan.priority.region_mode`

Controls how ScreenScraper applies `scan.priority.region` when picking regional media. With the default `prefer_rom_tags`, the region tags in the ROM's own filename win and `scan.priority.region` only reorders those tags. With `prefer_config`, the configured regions come first, so you can pull the FR box for an `(Europe)` dump even when `fr` is not in the filename, then fall back to the ROM's tags when a preferred region has no media.

**Default:** `prefer_rom_tags`

```yaml
scan:
    priority:
        region:
            - "fr"
            - "eu"
        region_mode: "prefer_config"
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

Which media types to fetch during a scan, primarily for ScreenScraper and the gamelist.xml importer.

<!-- prettier-ignore -->
!!! tip "This controls the UI Boxart styles"
    The gallery's **Boxart style** picker (2D Box, 3D Box, Physical, Mix Image) only changes what the cards *display*g. Styles other than 2D Box need their media type added here, then a rescan, or the cards fallback to 2D Box. See [Boxart styles and media types](../getting-started/metadata-providers.md#boxart-styles-and-media-types) for the full mapping and steps.

| Type               | Description                                  |
| ------------------ | -------------------------------------------- |
| `box2d`            | Normal 2D cover art. Always enabled.         |
| `box2d_back`       | Back cover art.                              |
| `box2d_side`       | 2D side/spine box art.                       |
| `box3d`            | 3D box art.                                  |
| `miximage`         | Composite image (box + screenshot + logo).   |
| `miximage_v2`      | Newer composite-image layout.                |
| `physical`         | Physical media (disc, cartridge).            |
| `screenshot`       | In-game screenshot. Enabled by default.      |
| `title_screen`     | Title-screen capture.                        |
| `marquee`          | Transparent logo.                            |
| `logo`             | Clear/wheel logo art.                        |
| `fanart`           | Community-uploaded fan art.                  |
| `bezel`            | EmulatorJS-compatible bezel.                 |
| `manual`           | PDF manual. Enabled by default.              |
| `video`            | Gameplay video (big files, watch your disk). |
| `video_normalized` | Loudness-normalised gameplay video.          |

```yaml
scan:
    media:
        - box2d
        - screenshot
        - manual
        - bezel
```

### `scan.gamelist.export`

Generate a `gamelist.xml` in each platform folder, compatible with ES-DE/Batocera.

```yaml
scan:
    gamelist:
        export: true
        media:
            thumbnail: box2d
            image: screenshot
```

`media.thumbnail` and `media.image` pick which [`scan.media`](#scanmedia) type fills the `<thumbnail>` and `<image>` tags.

### `scan.pegasus.export`

Export metadata in Pegasus-frontend format (`metadata.pegasus.txt`).

```yaml
scan:
    pegasus:
        export: true
```

Both exports are covered in full in [Exports](exports.md).

---

## `emulatorjs`

These keys tune the in-browser EmulatorJS player for every user on your instance. The end-user side lives in [In-Browser Play → EmulatorJS](../using/in-browser-play/emulatorjs.md). To disable EmulatorJS altogether (e.g. when running headless with companion apps only), set `DISABLE_EMULATOR_JS=true` in your env vars.

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

Multi-disc games hand EmulatorJS every disc at once, which lets the emulator swap between them from its own menu without a reload. Set this to go back to booting only the disc you launched, which is worth trying if a core doesn't cope with the batch.

**Default:** `false`

```yaml
emulatorjs:
    disable_batch_bootup: true
```

### `emulatorjs.default_cores`

Preselect the libretro core for a platform, keyed by [platform slug](../platforms/supported-platforms.md). Players who have already chosen a core on their device will keep defaulting to it.

```yaml
emulatorjs:
    default_cores:
        nds: desmume
        nintendo-dsi: melonds
```

Core names have to be exact, and anything you don't list keeps EmulatorJS's own default.

### `emulatorjs.auto_save_sync`

Upload a save every time the emulator writes one, rather than only on save-and-quit. Closing the tab or suffering a crash mid-game then loses nothing.

**Default:** `false`

```yaml
emulatorjs:
    auto_save_sync: true
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

### Server owner vs per-user

Most settings under `emulatorjs.settings` and `emulatorjs.controls` can be overridden by users in-game (Menu → Settings, Menu → Controls). Per-user values take precedence, the config.yml setting is the fallback.

| Where the setting lives             | Who it affects       | Survives upgrades? |
| ----------------------------------- | -------------------- | ------------------ |
| Server owner: `config.yml`/env vars | Everyone, as default | Yes                |
| Per-user: in-game Menu → Settings   | Just that user       | Yes                |
| Per-user: in-game Menu → Controls   | Just that user       | Yes                |

---

## `streaming`

Configure [emulator streaming](../using/emulator-streaming.md), which lets you launch games in native emulator containers and stream them to the browser. The end-user side and full setup walkthrough live in [Using RomM → Emulator Streaming](../using/emulator-streaming.md).

### `streaming.enabled`

**Default:** `false`

```yaml
streaming:
    enabled: true
```

### `streaming.containers`

**One entry per container**, not per platform. A container serves every platform listed in its `platforms` map, and its own keys are the defaults for all of them.

| Key                | Required | Purpose                                                                                                         |
| ------------------ | -------- | --------------------------------------------------------------------------------------------------------------- |
| `host`             | Yes      | Browser-facing Selkies web UI, served over **HTTPS**, or a path when reverse proxied onto RomM's own origin     |
| `platforms`        | Yes      | Map of [platform slug](../platforms/supported-platforms.md) to the emulator serving it, or to an override block |
| `protocol`         | Yes      | `webstation`. Omitted, the entry is read as a deprecated per-emulator broker mod                                |
| `label`            | Yes      | Name for the container, used on the play action for any platform that sets none of its own                      |
| `subfolder`        | No       | URL prefix the broker is served under, matching the container's `SUBFOLDER`                                     |
| `broker_host`      | No       | Server-to-broker API base. Derived from `host` when omitted, and **required** when `host` is a path             |
| `broker_secret`    | No       | Secret for this container, used only when the `STREAMING_BROKER_SECRET` env var is unset                        |
| `library_path`     | No       | In-container path to the RomM library, if it is mounted somewhere other than the default `/romm/library`        |
| `emulator`         | No       | Lowercased name grouping this container's states and memory cards, defaults to `label`                          |
| `memory_card_sync` | No       | Sync the whole memory card to the RomM library, honoured on `ps2` and `ngc` and ignored elsewhere               |

Each `platforms` value is either the emulator name on its own, or a block overriding `emulator`, `label` and `memory_card_sync` for that platform.

```yaml
streaming:
    enabled: true
    containers:
        - protocol: webstation
          host: https://192.168.1.56:3010 # browser-facing, must be HTTPS
          subfolder: /streaming # matches the container's SUBFOLDER
          library_path: /romm # where it mounts your ROM library
          broker_secret: change-me # matches the container's BROKER_SECRET
          label: Emulation station
          platforms:
              snes: retroarch # the emulator name directly...
              ps2: # ...or a block overriding container keys
                  emulator: pcsx2
                  label: PCSX2
                  memory_card_sync: true
              ngc:
                  emulator: dolphin
                  label: Dolphin
                  memory_card_sync: true
```

Platforms listed on several containers form a pool, with each claim taking the first free lane. Pool members have to agree on `emulator`, `memory_card_sync` and `protocol`, and are differentiated by broker host, so give each one a distinct `broker_host` (see [Emulator Streaming → How a session works](../using/emulator-streaming.md#how-a-session-works)).

See [Emulator Streaming → Memory cards](../using/emulator-streaming.md#memory-cards) for how `memory_card_sync` behaves, and [Migrating to webstation](../using/emulator-streaming-migration.md) if you still run the per-emulator broker mods.

---

## Related

- [Folder Structure](../getting-started/folder-structure.md): how the filesystem shape interacts with `config.yml`
- [Metadata Providers](../getting-started/metadata-providers.md): per-provider detail for the `scan.priority.*` slugs
- [Emulator Streaming](../using/emulator-streaming.md): the full setup guide for the `streaming` block
