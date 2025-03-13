---
title: Troubleshooting Scanning
description: Troubleshooting issues relating to library scanning
---

### Scan is skipping all platforms/ends instantly

There are a few common reasons why a scan may end instantly/without scanning platforms

- Badly mounted library: verify that you mounted your ROMs folder at `/romm/library`
- Incorrect permissions: the app needs to read the files and folders in your library, check their permissions with `ls -lh`
- Invalid folder structure: verify that your folder structure matches the one in the [README](https://github.com/rommapp/romm#-folder-structure)

### ROMs not found for platform X, check `romm` folder structure

This is the same issue as the one above, and can be quickly solved by verifying your folder structure. RomM expects a library with a folder named `roms` in it, for example:

- `/server/media/library:/romm/library`
- `/server/media/games/roms:/romm/library/roms`

### Scan does not recognize a platform

When scanning the folders mounted in `/library/roms`, the scanner tries to match the folder name with the platform's slug in IGDB. If you notice that the scanner isn't detecting a platform, verify that the folder name matches the slug in the URL of the [platform in IGDB](https://www.igdb.com/platforms). For example, the Nintendo 64DD has the URL <https://www.igdb.com/platforms/64dd>, so the folder should be named `64dd`.

### Scan times out after ~4 hours

The background scan task times out after 4 hours, which can happen if you have a very large library. The easiest work around is to keep running scans every 4 hours, **without** checking the "Complete re-scan" option.
