<!-- trunk-ignore-all(markdownlint/MD033) -->
<!-- trunk-ignore-all(markdownlint/MD041) -->

Below is a breakdown of each section of the `config.yml` file and its purpose. You can find a full example of the file in the [config.example.yml](https://github.com/rommapp/romm/blob/master/examples/config.example.yml) file.

---

## Exclude Section

Control which platforms, ROMs, or files to ignore during scanning.

### Platforms

Exclude entire platforms (folders) from being scanned.

**Example:**

```yaml
exclude:
    platforms: ["ps", "ngc", "gba"]
```

### ROMs

Fine-tune which ROMs or files are excluded.

#### Single File ROMs

Applies to ROMs that are single files (not in subfolders).

- **extensions**: Exclude files by extension
- **names**: Exclude files by name or pattern (supports Unix wildcards)

**Example:**

```yaml
exclude:
    roms:
        single_file:
            extensions: ["xml", "txt"]
            names: ["info.txt", "._*", "*.nfo"]
```

#### Multi-File ROMs

Applies to ROMs stored as folders (multi-disc, with DLC, etc.).

- **names**: Exclude entire folders by name
- **parts.names**: Exclude files by name or pattern from within multi-file ROM folders
- **parts.extensions**: Exclude files by extension from within multi-file ROM folders

**Example:**

```yaml
exclude:
    roms:
        multi_file:
            names: ["final fantasy VII", "DLC"]
            parts:
                names: ["data.xml", "._*"]
                extensions: ["xml", "txt"]
```

---

## System Section

Customize how RomM interprets your folder and platform names.

### Custom Folder Names

Map your custom folder names to RomM's recognized platform names.

**Example:**

```yaml
system:
    platforms:
        gc: "ngc" # Treats 'gc' folder as GameCube
        psx: "ps" # Treats 'psx' folder as PlayStation
```

### Versions

Associate a platform with its main version. This also tells RomM to fetch metadata from the main version source.

**Example:**

```yaml
system:
    versions:
        naomi: "arcade"
```

---

## Filesystem Section

Specify the folder name where your ROMs are located if it differs from the default.

**Example:**

If your ROMs folder is named `my_roms` instead of `roms`:

```yaml
filesystem:
    roms_folder: "my_roms"
```

---

## Scan Section

Configure metadata scanning priorities and media assets to download.

### Priority

Customize the order in which metadata providers are queried during scans.

#### Metadata

Controls metadata provider priority order.

**Provider list in default order:**

- `igdb` - IGDB (highest priority)
- `moby` - MobyGames
- `ss` - Screenscraper
- `ra` - RetroAchievements
- `launchbox` - Launchbox
- `gamelist` - ES-DE gamelist.xml
- `hasheous` - Hasheous
- `flashpoint` - Flashpoint Project
- `hltb` - HowLongToBeat (lowest priority)

**Example:**

```yaml
scan:
    priority:
        metadata:
            - "igdb"
            - "ss"
            - "moby"
```

#### Artwork

Controls artwork provider priority order for cover art and screenshots.

**Default:** Same as `priority.metadata`

**Example:**

```yaml
scan:
    priority:
        artwork:
            - "igdb"
            - "ss"
            - "moby"
```

#### Region

Sets preferred region for cover art and game title (Screenscraper only).

**Default:** `["us", "wor", "ss", "eu", "jp"]`

**Example:**

```yaml
scan:
    priority:
        region:
            - "us"
            - "eu"
            - "jp"
```

#### Language

Sets preferred language for cover art and game title (Screenscraper only).

**Default:** `["en", "fr"]`

**Example:**

```yaml
scan:
    priority:
        language:
            - "en"
            - "es"
            - "fr"
```

### Media

Configures which media assets to download (Screenscraper and ES-DE gamelist.xml only).

**Media types:**

- `box2d` - Normal cover art (always enabled)
- `box3d` - 3D box art
- `miximage` - Mixed image of multiple media
- `physical` - Disc, cartridge, etc.
- `screenshot` - Screenshot (enabled by default)
- `title_screen` - Title screen
- `marquee` - Transparent logo
- `fanart` - User uploaded artwork
- `bezel` - Bezel displayed around the EmulatorJS window
- `manual` - Manual in PDF format (enabled by default)
- `video` - Gameplay video (warning: large file size)

**Example:**

```yaml
scan:
    media:
        - box2d
        - screenshot
        - manual
        - bezel
```

---

## EmulatorJS Section

Configure EmulatorJS per-core options and controls.

### Debug

Enable debug mode to log available options to the browser console.

**Example:**

```yaml
emulatorjs:
    debug: true
```

### Cache Limit

Cache limit per ROM in bytes. Set to `null` for unlimited.

**Example:**

```yaml
emulatorjs:
    cache_limit: 52428800 # 50 MB
```

### Settings

Configure core-specific settings. Use `default` to apply settings to all cores.

**Example:**

```yaml
emulatorjs:
    settings:
        parallel_n64: # Use the exact core name
            vsync: disable
        snes9x:
            snes9x_region: ntsc
        default: # These settings apply to all cores
            fps: show
```

### Controls

Map keyboard and controller controls for each player.

**Example (2-player SNES):**

```yaml
emulatorjs:
    controls:
        snes9x:
            0: # Player 1
                0: # Button mapping
                    value: x # Keyboard mapping
                    value2: BUTTON_2 # Controller mapping
            1: # Player 2
                0:
                    value: /
                    value2: BUTTON_2
```

See [EmulatorJS documentation](https://emulatorjs.org/docs4devs/control-mapping/) for control mapping details.

---

<!-- prettier-ignore -->
!!! tip
    You can find examples of full binded <a href="https://github.com/rommapp/romm/blob/master/examples/config.batocera-retrobat.yml" target="_blank" rel="noopener noreferrer">batocera</a> or <a href="https://github.com/rommapp/romm/blob/master/examples/config.es-de.example.yml" target="_blank" rel="noopener noreferrer">es-de</a> config files.

<!-- prettier-ignore -->
!!! warning
    Only uncomment or add the lines you need. Any omitted or empty sections will use RomM's defaults.

For a full example, see the <a href="https://github.com/rommapp/romm/blob/master/examples/config.example.yml" target="_blank" rel="noopener noreferrer">config.example.yml</a> file.
