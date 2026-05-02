---
title: Exports
description: Export metadata for use in other frontend
---

# Exports

Library metadata can be emitted in formats other frontends expect, for setups where this is the library authority and a separate frontend (ES-DE, Batocera, Pegasus) is the actual launcher.

## gamelist.xml (ES-DE/Batocera/RetroBAT)

ES-DE, Batocera, and compatibles look for a `gamelist.xml` in each platform folder, and these can be generated automatically.

**Enable via `config.yml`**

```yaml
scan:
    gamelist:
        export: true
        media:
            thumbnail: box2d # which media type to use as thumbnail
            image: screenshot # which as full image
```

With `export: true`, every scan writes a `gamelist.xml` into the platform folder, and downloads the selected media into sibling folders (`covers/`, `screenshots/`, etc.) that ES-DE expects.

Standard ES-DE/EmulationStation format:

```xml
<gameList>
  <game>
    <path>./metroid.nes</path>
    <name>Metroid</name>
    <desc>...</desc>
    <releasedate>19861115T000000</releasedate>
    <developer>Nintendo R&amp;D1</developer>
    <publisher>Nintendo</publisher>
    <genre>Action-Adventure</genre>
    <image>./screenshots/metroid.png</image>
    <thumbnail>./covers/metroid.png</thumbnail>
  </game>
  ...
</gameList>
```

### API endpoint

Trigger an export on demand:

```http
POST /api/export/gamelist-xml
Authorization: Bearer <token>
Content-Type: application/json

{
  "platforms": ["snes", "nes"]   // empty = all
}
```

Response includes where the files were written.

### Using with ES-DE

Once `gamelist.xml` has been generated and populated `covers/` + `screenshots/`, point ES-DE at the library:

```xml
<string name="MediaDirectory" value="/path/to/ROMs/folder" />
<bool name="LegacyGamelistFileLocation" value="true" />
```

- `MediaDirectory`: point it at the ROM folder (same path ES-DE uses for `ROMDirectory`), so ES-DE looks for media in-place rather than in its own library.
- `LegacyGamelistFileLocation`: makes ES-DE write updates back to the same `gamelist.xml` read on import, rather than its separate config dir.

See also [Metadata Providers → gamelist.xml](../administration/metadata-providers.md) for the _import_ direction (reading gamelist.xml back in).

## Pegasus

[Pegasus](https://pegasus-frontend.org/) is an alternative gaming frontend with its own metadata format. A `metadata.pegasus.txt` can be emitted per platform.

**Enable via `config.yml`**

```yaml
scan:
    pegasus:
        export: true
```

Human-readable text format:

```text
collection: Super Nintendo
shortname: snes
launch: /usr/bin/snes9x "{file.path}"

game: Super Metroid
file: /roms/snes/Super Metroid (USA).sfc
description: ...
developer: Nintendo R&D1
publisher: Nintendo
genre: Action-Adventure
release: 1994-03-19
assets.box: ./covers/Super Metroid.png
assets.screenshot: ./screenshots/Super Metroid.png
```

### API request

```http
POST /api/export/pegasus
Authorization: Bearer <token>
Content-Type: application/json

{
  "platforms": ["snes", "nes"]
}
```

## Re-running on changes

Exports don't auto-rerun on every metadata edit, instead they run:

- **Next scan**: exports are part of scan completion when enabled.
- **Manual trigger** via the API above

## See also

- [Configuration File → `scan.gamelist`](../reference/configuration-file.md#scangamelistexport-new-in-50)
- [Configuration File → `scan.pegasus`](../reference/configuration-file.md#scanpegasusexport-new-in-50)
