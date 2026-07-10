---
title: ROM Patcher
description: Apply IPS, UPS, BPS, PPF, and other patch formats on the server
---

# ROM Patcher

The **ROM Patcher** applies a patch file (translation, hack, rebalance, no-intro fix) to a ROM **on the server**: no CLI, no local tooling, and no uploading half-patched files by hand. It's a **Patcher tab** on the game's detail page, powered by patcherjs.

<!-- prettier-ignore -->
!!! note "Server-side patching (5.0+)"
    Earlier versions patched in the browser. As of 5.0, patching runs entirely on the server: you pick a base ROM and a patch from your library, RomM applies it server-side, and streams the result back. This removes the browser-memory ceiling that used to break large ISOs.

## How it works

1. Open a game and switch to the **Patcher** tab.
2. **Choose ROM**: pick the base game file. If the ROM has a single game file, it's selected for you.
3. **Choose patch**: pick the patch file. The patch has to be in your library, so either select an existing one (search the library, or pick from files already attached to the ROM) or **drag & drop / browse** to add a patch file first. RomM recognises a file as a patch by its `patch` category or a [supported extension](#supported-patch-formats).
4. Optionally set an **Output filename**. If left blank, RomM derives one as `<rom> (patched-<patch>)` with the ROM's original extension.
5. Pick what to do with the result (see [Output options](#output-options)) and hit **Apply**.

The patch's source checksum is validated against the ROM. If it doesn't match, RomM still returns a file but warns you that the patched output may be incorrect.

## Output options

Choose one or both:

- **Download patched ROM**: streams the patched file to your browser. Available to anyone who can view the ROM.
- **Upload to RomM**: saves the patched ROM back into the library. You pick a target **platform**, RomM stores the file in that platform's folder, and a **scan starts automatically** to pick it up as a new entry.

Metadata isn't inherited, so an uploaded patched ROM is **unmatched** until that scan matches it.

Uploading requires write access; users without it only see the download option.

## Supported patch formats

| Extension | Purpose                                                  |
| --------- | -------------------------------------------------------- |
| `.ips`    | International Patching System. Oldest + most common.     |
| `.ups`    | Universal Patching System. Successor to IPS.             |
| `.bps`    | Binary Patch System. Modern, preferred for ROM hacks.    |
| `.ppf`    | PlayStation Patch Format. For PSX/Saturn/Dreamcast ISOs. |
| `.rup`    | Retroarch Universal Patch.                               |
| `.aps`    | GBA-focused patch format.                                |
| `.bdf`    | Binary diff format.                                      |
| `.pmsr`   | Paper Mario Star Rod.                                    |
| `.vcdiff` | Generic binary diff (xdelta).                            |

If your patch has an unusual extension, try renaming to one of the above. Many are just different framings of the same underlying algorithm.

## Permissions

| Action                    | Scope required |
| ------------------------- | -------------- |
| Apply patch → download    | `roms.read`    |
| Apply patch → upload back | `roms.write`   |

## Limits

- **File size**: the ROM and the patch must each stay under `ROM_PATCHER_MAX_FILE_SIZE_BYTES` (default **4 GiB**). patcherjs loads the whole file into memory server-side, so oversized inputs are rejected with a `400`.
- **Multi-file ROMs**: for multi-disc games, patch each ISO separately.
- **Encrypted ROMs**: if the patch was authored against a decrypted ROM (e.g. DS `.nds` vs raw cartridge), your source has to match.
- **Save format changes**: patches that alter save-data layout will invalidate existing save files. Back them up before applying.

## Troubleshooting

- **"Unsupported patch format"**: the patch extension isn't in the [supported list](#supported-patch-formats), or the file is corrupted. Try re-downloading, or rename to the correct extension.
- **"Patch source checksum did not match the ROM"**: the patch was built against a different ROM revision than yours, common with no-intro vs TOSEC dumps. The output may be wrong even though a file was produced.
- **`400` on apply**: usually the ROM or patch exceeds `ROM_PATCHER_MAX_FILE_SIZE_BYTES`. Raise the limit (env var) or patch outside RomM.
- **Uploaded patched ROM stays unmatched**: expected until the automatic scan finishes matching it. Re-run a scan if it doesn't pick up.
