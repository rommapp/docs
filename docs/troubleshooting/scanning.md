---
title: Scanning Troubleshooting
description: Diagnose and fix library-scan problems
---

# Scanning Troubleshooting

Most scan problems boil down to the library not being mounted where expected, an incorrect folder structure, or a metadata provider being temporarily unavailable.

## Scan ends instantly/no platforms found

Three common causes:

1. **Library mounted in the wrong place**: The library is expected at `/romm/library` inside the container. Verify with `docker exec romm ls /romm/library`: you should see your `roms/` directory (Structure A) or platform folders (Structure B).
2. **Permissions**: the container has to read the files, so check from the host with `ls -lh /path/to/library`. If the scanner can't see them, nothing scans.
3. **Invalid folder structure**: review [Folder Structure](../getting-started/folder-structure.md). Structure A is tried first, so if it finds neither layout the scan completes in seconds with nothing found.

## "ROMs not found for platform X, check romm folder structure"

Common mount-path mistakes:

```yaml
# WRONG: mounts the platform folder itself
- /server/media/games/snes:/romm/library

# WRONG: skips the roms/ layer entirely
- /server/media/games:/romm/library

# CORRECT: mounts the parent of roms/
- /server/media/library:/romm/library # if library/ contains roms/
- /server/media/games/roms:/romm/library/roms # if you want to be explicit
```

## Platform folder isn't detected

Platform folder names are matched against IGDB platform slugs, so if your folder is named differently, it won't match.

Example: Nintendo 64DD's IGDB slug is `64dd` ([igdb.com/platforms/64dd](https://www.igdb.com/platforms/64dd)), so the folder should be named `64dd/`. If your folder is `n64dd/` or `nintendo-64dd/`, it won't detect.

Two fixes:

- **Rename the folder** to match the IGDB slug.
- **Add a binding** in `config.yml` to map your custom name onto the canonical slug:

```yaml
system:
    platforms:
        n64dd: "64dd" # your-folder-name: canonical-slug
```

See the [full list of supported slugs](../platforms/supported-platforms.md).

## Scan times out at ~4 hours

Scans are capped, so if yours hits the cap:

1. **Use `Quick` mode** from the Scan page, which skips already-catalogued files so most repeated scans complete in minutes.
2. **Raise the cap** if you need to run longer scans, set `SCAN_TIMEOUT=86400` (24 hours in seconds).
3. **Run scans per-platform** instead of everything at once, to checkpoint progress.

## Scan stops mid-platform

Check logs:

```sh
docker logs romm 2>&1 | grep -E 'ERROR.*scan_handler'
```

Log lines look like:

```text
ERROR:    [RomM][scan_handler][2025-04-12 11:48:55]   Failed to process /romm/library/roms/dos/game.zip: ...
```

## Lots of ROMs are unmatched

Options, in order of effort:

1. **Add more providers**: a ROM IGDB doesn't know about might be in ScreenScraper, Hasheous, or LaunchBox, so enable one or more, then run an **Unmatched** scan.
2. **Use filename tags**: if you already know the provider ID, rename the file to include `(igdb-1234)` or similar (see [Metadata Providers → Filename tags](../administration/metadata-providers.md#metadata-tags-in-filenames)).
3. **Manually match**: open the ROM detail page, click the **Match** button, and search for the right title.

## Hash calculations are slow

Hashing large ROMs (PS1, Saturn, DC images) is IO-bound, with a few options:

- **Skip hashing on small hosts**: set `filesystem.skip_hash_calculation: true` in `config.yml`, though you'll lose RetroAchievements and Hasheous matching since both depend on hashes.
- **Use SSD/NVMe for the library** if you care about hash performance.
- **Raise `SEVEN_ZIP_TIMEOUT`** if you're scanning many large `.7z` archives.
