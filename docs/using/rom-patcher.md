---
title: ROM Patcher
description: Apply IPS, UPS, BPS, PPF, and other patch formats in your browser
---

# ROM Patcher

The **ROM Patcher** applies a patch file (translation, hack, rebalance, no-intro fix) to a ROM **in your browser**: no CLI, no downloads, and no uploading half-patched files by hand.

## Supported patch formats

| Extension             | Purpose                                                  |
| --------------------- | -------------------------------------------------------- |
| `.ips`                | International Patching System. Oldest + most common.     |
| `.ups`                | Universal Patching System. Successor to IPS.             |
| `.bps`                | Binary Patch System. Modern, preferred for ROM hacks.    |
| `.ppf`                | PlayStation Patch Format. For PSX/Saturn/Dreamcast ISOs. |
| `.rup`                | Retroarch Universal Patch.                               |
| `.aps`                | GBA-focused patch format.                                |
| `.bdf`                | Binary diff format.                                      |
| `.pmsr`               | Paper Mario Star Rod.                                    |
| `.vcdiff` (`.xdelta`) | Generic binary diff.                                     |

If your patch has an unusual extension, try renaming to one of the above. Many are just different framings of the same underlying algorithm.

## Patching options

Two output paths:

- **Download patched ROM**: saves a file locally, nothing leaves your machine as everything runs client-side.
- **Save to library**: Store the patched ROM in your library. Goes in the same platform folder as the original, with the patched filename, where the next scan will pick it up as a new entry.

Metadata isn't inherited, so the new ROM is **unmatched** until you run a scan!

## Permissions

| Action                        | Viewer | Editor | Admin |
| ----------------------------- | :----: | :----: | :---: |
| Use Patcher → Download        |   ✓    |   ✓    |   ✓   |
| Use Patcher → Save to library |   -    |   ✓    |   ✓   |

Saving to the library requires `roms.write` scope.

## Limits

- **Browser memory**: huge ROMs (PSX/Saturn/PSP ISOs, > 1 GB) can struggle in browsers with low memory limits. Safari is the most restrictive but Firefox/Chrome can handle bigger files.
- **Multi-file ROMs**: for multi-disc games, patch each ISO separately.
- **Encrypted ROMs**: if the patch was authored against a decrypted ROM (e.g. DS `.nds` vs raw cartridge), your source has to match.
- **Save format changes**: patches that alter save-data layout will invalidate existing save files. Back them up before applying.

## Troubleshooting

- **"Invalid patch format"**: wrong extension or corrupted file, try re-downloading the patch.
- **"Checksum mismatch"**: the patch was built against a different ROM revision than yours, common with no-intro vs TOSEC dumps.
- **Browser hangs on huge ROMs**: close other tabs, try Firefox, or patch outside the browser with `Floating IPS` or `BPS` CLI tools then upload the result.
- **"Save to library" produces a broken ROM**: usually the patcher succeeded but the file was corrupted in transit.
