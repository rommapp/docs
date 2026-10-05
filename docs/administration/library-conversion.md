---
title: Library Conversion
description: Convert your library to compressed formats with rom-converto
---

# Library Conversion

Disc and cartridge images can be converted between formats with [rom-converto](https://github.com/DevYukine/rom-converto), in two ways:

- **Library conversion** rewrites the files in your library to one storage format per platform, such as CHD for PlayStation or RVZ for GameCube, to save disk space.
- **Download conversion** leaves the library alone and converts a single download to a format the client asks for, for a handheld or emulator that can't read the stored one.

## Enabling rom-converto

Set `ROM_CONVERTO_ENABLED=true` and restart the container. The CLI is probed on first use and its version logged. If the probe fails, a warning is logged and conversion stays off until the next restart.

| Variable                       | Default | Description                                                         |
| ------------------------------ | ------- | ------------------------------------------------------------------- |
| `ROM_CONVERTO_ENABLED`         | `false` | Enable the Convert library task and `?format=` download conversions |
| `ROM_CONVERTO_TIMEOUT`         | `600`   | Seconds each rom-converto operation may run                         |
| `ROM_CONVERTO_MAX_CONCURRENCY` | `2`     | Concurrent conversions per web or task worker                       |

With it enabled, scans also use the CLI to read title IDs and serials from the files of supported platforms (3DS, DS, PSP, PS Vita, PlayStation, PS2, PS3, GameCube, Wii, Wii U, Switch, Switch 2, Xbox and Xbox 360), which you can turn off with [`converto.scan_metadata`](#configuration).

## Configuration

Admins set these options on the **Conversion settings** page, which writes them to the `converto` section of [`config.yml`](../reference/configuration-file.md#converto). You can also edit that section by hand:

```yaml
converto:
    download_conversion_enabled: true
    platform_formats:
        psx: chd
        ps2: chd
        ngc: rvz
        wii: rvz
        switch: nsz
```

| Key                           | Default | Description                                                                                                 |
| ----------------------------- | ------- | ----------------------------------------------------------------------------------------------------------- |
| `download_conversion_enabled` | `false` | Offer converted downloads through `?format=`                                                                |
| `platform_formats`            | `{}`    | Library format per platform slug, used by the Convert library task. A platform left out is never converted. |
| `cache_max_size_gb`           | `20`    | Size cap of the converted download cache, in GB. `0` leaves it unbounded.                                   |
| `cache_ttl_hours`             | `24`    | Hours a converted download stays cached after it was last served (at least `1`)                             |
| `scan_metadata`               | `true`  | Read title IDs with rom-converto during scans                                                               |

`cache_ttl_hours` and `scan_metadata` are only set in `config.yml`, and the settings page keeps whatever value they have there. An invalid value in this section stops RomM from starting, with an `Invalid config.yml: converto...` log line. For `platform_formats`, that's a platform rom-converto can't store or a format that isn't one of its library formats, and the log line lists the valid options.

## Library formats

Only lossless conversions are offered as library formats, so a converted game holds the same data as the original:

| Platform                                | Slug                            | Library formats            |
| --------------------------------------- | ------------------------------- | -------------------------- |
| Nintendo 3DS                            | `3ds`                           | `z3ds`, `cia`, `cci`       |
| PlayStation Portable                    | `psp`                           | `chd`, `cso`, `zso`, `iso` |
| PlayStation 2                           | `ps2`                           | `chd`, `cso`, `zso`, `iso` |
| PlayStation, Saturn, Sega CD, Dreamcast | `psx`, `saturn`, `segacd`, `dc` | `chd`                      |
| GameCube                                | `ngc`                           | `rvz`, `iso`               |
| Wii                                     | `wii`                           | `rvz`, `iso`, `wbfs`       |
| Switch, Switch 2                        | `switch`, `switch-2`            | `nsz`, `xcz`, `nsp`, `xci` |
| Xbox 360                                | `xbox360`                       | `zar`                      |

Each format accepts its own source files: CHD is made from `.cue` sheets or `.iso` images (and for PSP and PS2 also from `.cso`, `.zso` and `.dax`), RVZ from GameCube `.iso`, `.gcm`, `.gcz` and NKit images or Wii `.iso`, `.wbfs`, `.wia`, `.gcz` and NKit images, and NSZ from `.nsp`. A file with no route to the chosen format is counted as unsupported and left alone. The `iso`, `cia`, `cci`, `nsp`, `xci` and `wbfs` targets are uncompressed, so converting to one of them can grow your library rather than shrink it.

## The Convert library task

**Convert library** is a manual [task](scheduled-tasks.md) that converts every game on a platform with a library format, in place:

- Only matched games are converted, and unidentified ones are skipped because a converted file no longer hash-matches a DAT, so match them first.
- Games keep their identity: the database entry is updated to point at the new file, so saves, states, collections, notes and play history carry over. In a multi-file game, the `.m3u` playlists beside the files are rewritten to the new names.
- Originals are deleted once their conversion succeeds and the game points at the new file. A conversion that fails, or whose output name is already taken, keeps the original.
- A `.cue` sheet converts with its `.bin` tracks, which are deleted along with it. A cue that shares tracks with another cue, or references a file outside its folder, is refused.

Because it deletes files, the task is flagged as **destructive**, and the UI asks you to type a confirmation before it runs. It's also single-instance, so asking to run it again while it's queued or running returns `409 Conflict`. A full run can take hours on a large library, bounded per file by `ROM_CONVERTO_TIMEOUT`. When it finishes, the task reports how many files it converted, skipped as already converted, unmatched or unsupported, and failed, and how many bytes it saved.

**Back up your library before the first run!**

## Download conversion

With `download_conversion_enabled` on, a client can ask for a single-file download in another format by adding `?format=` to the download URL, with a comma-separated list of formats it can read in order of preference:

```text
GET /api/roms/{id}/content/{file_name}?format=zso,iso
```

The response is one of:

| Response                     | When                                                                                          |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| `200` with the stored file   | The stored file is already in one of the listed formats                                       |
| `200` with a converted copy  | A cached conversion exists, or a new one finishes within about 15 seconds                     |
| `202` with `Retry-After: 30` | A conversion is running. Repeat the request after the delay.                                  |
| `406 Not Acceptable`         | No listed format can be produced, the request covers more than one file, or conversion is off |

`HEAD` on the same URL reports the same outcome without starting a conversion. A conversion started by a download keeps running when the client stops waiting, and its result lands in the cache for the next request.

Any format rom-converto can reach from the stored file is allowed here, lossy ones included. `DetailedRomSchema.download_formats` lists the formats the caller can request for a game, which is empty for multi-file games, when conversion is off, and for callers who can't start a conversion. Only signed-in users can start one, so visitors in [kiosk mode](authentication.md) or on an unauthenticated download endpoint (`DISABLE_DOWNLOAD_ENDPOINT_AUTH`) get a cached copy or a `406`. The web UI offers the same list as "Download as" on a game page.

### The conversion cache

Converted downloads are cached in `/romm/cache/converts`. A copy expires `cache_ttl_hours` after it was last served, and when the cache would grow past `cache_max_size_gb`, the least recently served copies are evicted first. The **Scheduled conversion cache cleanup** task removes expired copies every day at 04:00. A conversion that failed is remembered, so it isn't retried on every request until its cache entry expires.

## API

| Method        | Path                                         | Description                                                                                                 |
| ------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `PUT`         | `/api/config/converto_settings`              | Replace `download_conversion_enabled`, `cache_max_size_gb` and `platform_formats` (needs `platforms.write`) |
| `GET`         | `/api/config`                                | `CONVERTO` holds the current settings, and `CONVERTO_LIBRARY_TARGETS` the library formats per platform      |
| `GET`         | `/api/heartbeat`                             | `CONVERTO` reports whether rom-converto is enabled and available                                            |
| `POST`        | `/api/tasks/run/convert_library`             | Run the Convert library task (needs `tasks.run`)                                                            |
| `GET`, `HEAD` | `/api/roms/{id}/content/{file_name}?format=` | Download in a requested format                                                                              |
