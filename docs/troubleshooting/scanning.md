---
title: Scanning Troubleshooting
description: Diagnose and fix library-scan problems.
---

# Scanning Troubleshooting

Most scan problems boil down to: library not mounted where RomM expects, folder structure wrong, or a metadata provider being unreachable.

## Scan ends instantly / no platforms found

Three common causes:

1. **Library mounted in the wrong place.** RomM expects your library at `/romm/library` inside the container. Verify with `docker exec romm ls /romm/library`. You should see your `roms/` directory (Structure A) or platform folders (Structure B).
2. **Permissions.** The RomM container has to read the files. Check from the host: `ls -lh /path/to/library`. If the RomM process can't see them, nothing scans.
3. **Invalid folder structure.** Review [Folder Structure](../getting-started/folder-structure.md). RomM tries Structure A first, so if it finds neither layout, the scan completes in seconds with nothing found.

## "ROMs not found for platform X, check romm folder structure"

Same root cause as the previous one. RomM needs a `roms/` directory somewhere: either `/romm/library/roms/{platform}/` (Structure A) or `/romm/library/{platform}/roms/` (Structure B).

Common mount-path mistakes:

```yaml
# WRONG: mounts the platform folder itself
- /server/media/games/snes:/romm/library

# WRONG: skips the roms/ layer entirely
- /server/media/games:/romm/library

# CORRECT: mounts the parent of roms/
- /server/media/library:/romm/library      # if library/ contains roms/
- /server/media/games/roms:/romm/library/roms  # if you want to be explicit
```

## Platform folder isn't detected

RomM matches your platform folder names against IGDB platform slugs. If your folder is named differently, it won't match.

Example: Nintendo 64DD's IGDB slug is `64dd` ([igdb.com/platforms/64dd](https://www.igdb.com/platforms/64dd)), so the folder should be named `64dd/`. If your folder is `n64dd/` or `nintendo-64dd/`, it won't detect.

Two fixes:

- **Rename the folder** to match the IGDB slug.
- **Add a binding** in `config.yml` to map your custom name onto the canonical slug:

    ```yaml
    system:
      platforms:
        n64dd: "64dd"      # your-folder-name: canonical-slug
    ```

Full list of supported slugs: [Supported Platforms](../platforms/supported-platforms.md).

## Scan times out at ~4 hours (or whatever `SCAN_TIMEOUT` says)

Scans are capped. If yours hits the cap:

1. **Use `Quick` mode** from the Scan page: skips already-catalogued files. Most repeated scans complete in minutes.
2. **Raise the cap** if you need a full rescan: `SCAN_TIMEOUT_HOURS=8` (or whatever). See [Environment Variables](../reference/environment-variables.md).
3. **Run scans per-platform** instead of everything at once, to checkpoint progress.

## Scan stops mid-platform

Check logs:

```sh
docker logs romm 2>&1 | grep -E 'ERROR.*scan_handler'
```

Common culprits:

- **Corrupted file**: unzip it, re-zip, try again.
- **Old DOS zip with backslash paths**: Python's `zipfile` chokes on these. Re-create the archive with forward slashes.
- **Read errors on the mount**: usually SMB/NFS flakiness. Watch `dmesg` for mount drops.

Log lines look like:

```text
ERROR:    [RomM][scan_handler][2025-04-12 11:48:55]   Failed to process /romm/library/roms/dos/game.zip: ...
```

## Tracking progress on a big library

When scans run for hours across many platforms, the live UI log is hard to follow. Tail the container logs instead:

```sh
docker logs romm 2>/dev/null | grep -E 'scan_handler.*Identified as'
```

Sample output:

```text
INFO:     [RomM][scan_handler][2025-04-12 11:37:40]   Identified as PlayStation 🎮
INFO:     [RomM][scan_handler][2025-04-12 14:39:32]   Identified as DOS 🎮
INFO:     [RomM][scan_handler][2025-04-13 12:50:42]   Identified as WonderSwan 🎮
```

## Metadata provider errors

Check the scan log for per-provider errors:

- **IGDB: "Could not get twitch auth token"** → `IGDB_CLIENT_ID` or `IGDB_CLIENT_SECRET` is wrong, or revoked on the Twitch side.
- **ScreenScraper: "403 / DAILY_LIMIT_REACHED"** → you've hit the free-tier quota. Wait, or upgrade your ScreenScraper membership.
- **RetroAchievements: "Invalid API key"** → regenerate at [retroachievements.org/settings](https://retroachievements.org/settings).
- **Any provider: "Request timed out"** → transient. Re-run an **Unmatched** scan to retry only the failures.

Full provider reference: [Metadata Providers](../administration/metadata-providers.md).

## Lots of ROMs are unmatched

Options, in order of effort:

1. **Add more providers.** A ROM IGDB doesn't know about might be in ScreenScraper, Hasheous, or LaunchBox. Enable one or more, then run an **Unmatched** scan.
2. **Use filename tags.** If you already know the provider ID, rename the file to include `(igdb-1234)` or similar. See [Metadata Providers → Filename tags](../administration/metadata-providers.md#metadata-tags-in-filenames).
3. **Manually match.** Open the ROM detail page, click the **Match** button, and search for the right title.

## Hash calculations are slow

Hashing large ROMs (PS1, Saturn, DC images) is IO-bound. Options:

- **Skip hashing on small hosts**: check **Skip hash calculation** on the Scan page, or set `filesystem.skip_hash_calculation: true` in `config.yml`. You lose RetroAchievements and Hasheous matching (both depend on hashes).
- **Use SSD/NVMe for the library** if you care about hash performance.
- **Raise `SEVEN_ZIP_TIMEOUT`** if you're scanning many large `.7z` archives.

## Scan seems to work but nothing shows up

Refresh the page. The ribbons on the home dashboard cache aggressively during a scan. Still blank? Check **Administration → Server Stats**. If counts are zero, the scan didn't actually persist anything. Usually a DB permission issue, so check `docker logs romm 2>&1 | grep -i 'database'`.
