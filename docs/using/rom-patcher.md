---
title: ROM Patcher
description: Apply IPS, UPS, BPS, PPF, and other patch formats to a ROM in the browser.
---

# ROM Patcher

The **ROM Patcher** applies a patch file (a translation, hack, rebalance, no-intro fix) to a ROM **in your browser**: no CLI, no downloads, no uploading half-patched files by hand.

New in 5.0. Powered by the `rom-patcher-js` library.

## Supported patch formats

| Extension             | Purpose                                                      |
| --------------------- | ------------------------------------------------------------ |
| `.ips`                | International Patching System. Oldest + most common.         |
| `.ups`                | Universal Patching System. Successor to IPS.                 |
| `.bps`                | Binary Patch System. Modern, preferred for ROM hacks.        |
| `.ppf`                | PlayStation Patch Format. For PSX / Saturn / Dreamcast ISOs. |
| `.rup`                | Retroarch Universal Patch.                                   |
| `.aps`                | GBA-focused patch format.                                    |
| `.bdf`                | Binary diff format.                                          |
| `.pmsr`               | Paper Mario Star Rod.                                        |
| `.vcdiff` (`.xdelta`) | Generic binary diff.                                         |

If your patch has an unusual extension, try renaming to one of the above. Many are just different framings of the same underlying algorithm.

## Getting there

Menu bar → **Patcher** icon (a wrench). Admins and Editors can also reach it from the ROM detail page → context menu → **Patch this ROM**.

## Patching workflow

1. **Upload the ROM**: drag and drop, or click to browse. The Patcher validates basic structure.
2. **Upload the patch**: same drag/drop zone below.
3. **Pick the target platform**: usually auto-detected from the ROM.
4. **Choose output**:
    - **Download patched ROM**: saves a file locally. RomM keeps neither the original nor the result.
    - **Save to library**: adds the patched ROM as a new entry in your library, alongside the original
    - Optional **filename**: customise the output name. Defaults to `<original> [patched].<ext>`
5. **Apply**.

Everything runs client-side in the browser. The ROM never gets uploaded to the server during patching (if you picked Download), so nothing leaves your machine.

## Save to library

When you pick **Save to library** instead of Download, RomM receives the final patched file and stores it as a new ROM. Goes in the same platform folder as the original, with the patched filename. A subsequent scan picks it up, and a **Quick** scan is enough.

Metadata isn't inherited, so the new ROM is **unmatched** until you run a scan. If the patch is listed on IGDB / ROMHacking.net as its own entry, matching may pick it up. Otherwise, match manually or tag with `(igdb-XXXX)` (see [Metadata Providers → Filename tags](../administration/metadata-providers.md#metadata-tags-in-filenames)).

## Permissions

| Action                        | Viewer | Editor | Admin |
| ----------------------------- | :----: | :----: | :---: |
| Use Patcher → Download        |   ✓    |   ✓    |   ✓   |
| Use Patcher → Save to library |   -    |   ✓    |   ✓   |

Saving to the library requires `roms.write` scope.

## Typical workflows

### Translation patches

Many Japanese-only games have fan translations as IPS or BPS patches. Point the Patcher at the original ROM + translation, save to library, and you've got a new library entry alongside the original with the translated game, no clobbering.

### ROM hacks and rebalances

Kaizo Mario-type hacks, FF6 balance patches, etc., follow the same flow: the patched ROM gets its own entry, and your original stays intact.

### Regional fixes

No-intro patches, region-free patches. Apply, download, and verify with the Hash feature (upcoming) or externally.

## Limits

- **Browser memory**: huge ROMs (PSX / Saturn / PSP ISOs, > 1 GB) can struggle in browsers with low memory limits. Safari is the most restrictive but Firefox / Chrome handle bigger files.
- **Multi-file ROMs**: the Patcher operates on a single file. For multi-disc games, patch each ISO separately.
- **Encrypted ROMs**: if the patch was authored against a decrypted ROM (e.g. DS `.nds` vs raw cartridge), your source has to match.
- **Save format changes**: patches that alter save-data layout will invalidate existing save files. Back them up before applying.

## Verifying the result

The Patcher shows the pre-patch and post-patch hash (CRC32 + MD5) after apply. Compare against whatever the patch author published. If hashes match: you've got the correct patched ROM. If not: wrong source ROM, wrong patch, or the patch archive was truncated.

## Troubleshooting

- **"Invalid patch format"**: wrong extension or corrupted file. Try re-downloading the patch.
- **"Checksum mismatch"**: the patch was built against a different ROM revision than yours, common with no-intro vs TOSEC dumps. Look up the patch author's expected source.
- **Browser hangs on huge ROMs**: close other tabs, try Firefox, or patch outside the browser with `Floating IPS` or `BPS` CLI tools then upload the result.
- **"Save to library" produces a broken ROM**: usually the patcher succeeded but the file was corrupted in transit. Retry. If it persists, patch externally and upload.

## API

ROM patching is a client-side feature with no dedicated backend endpoints. When you "save to library", the patched file is uploaded via the standard chunked-upload flow (`POST /api/roms/upload/start` → `PUT /api/roms/upload/{id}` → `POST /api/roms/upload/{id}/complete`) (see [Uploads → API](uploads.md#api)).
