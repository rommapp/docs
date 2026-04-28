---
title: Igir Collection Manager
description: Clean up and normalise your ROM collection
---

# Igir Collection Manager

[Igir](https://igir.io/) is a zero-setup ROM collection manager that sorts, filters, extracts, archives, patches, and reports on collections of any size. While not a companion app per se, it's useful for cleaning up a library _before_ importing into RomM, so scans have a better-named, better-organised starting point.

**This is not an official app.** Igir is a separate community project. We document integration here because it's a common workflow and produces a compatible layout directly.

## When you'd use Igir

- You have a messy collection with inconsistent naming, mixed formats, dumps from multiple sources.
- You want to **match against No-Intro / Redump DAT files** to verify authenticity and standardise names.
- You want to **filter** only retail releases, or strip out hacks, or keep only one region, etc.
- You want to move / rename files to RomM's expected platform folder layout.

## Directory setup

Igir works on a copy of your ROMs (never in place) to let you iterate on its config without risking the originals.

```text
.
├── dats/                 # DAT files (No-Intro, Redump)
├── roms/                 # Your original ROM collection (untouched)
├── roms-unverified/      # Working copy Igir will process
└── igir-romm-cleanup.sh  # the script below
```

1. Make a working copy

```sh
cp -r roms/ roms-unverified/
```

2. Download DAT files

DAT files are hash-referenced catalogues Igir matches against.

- **Cartridge systems:** [No-Intro daily](https://datomatic.no-intro.org/index.php?page=download&op=daily), full DAT compilation
- **Optical systems (PS1, Saturn, etc.):** [Redump](http://redump.org/downloads/), per-platform DAT files

Drop the DAT files into `dats/`. You can use a subset if you only care about specific platforms.

## The cleanup script

Save as `igir-romm-cleanup.sh`:

```bash
#!/usr/bin/env bash
set -ou pipefail
cd "$(dirname "${0}")"

INPUT_DIR=roms-unverified
OUTPUT_DIR=roms-verified

# https://igir.io/
# DAT files: https://datomatic.no-intro.org/index.php?page=download&op=daily
time npx -y igir@latest \
  move \
  extract \
  report \
  test \
  -d dats/ \
  -i "${INPUT_DIR}/" \
  -o "${OUTPUT_DIR}/{romm}/" \
  --input-checksum-quick false \
  --input-checksum-min CRC32 \
  --input-checksum-max SHA256 \
  --only-retail
```

Make it executable:

```sh
chmod +x igir-romm-cleanup.sh
```

## Run

```sh
./igir-romm-cleanup.sh
```

## Manually migrate leftovers

Some ROMs won't be identified (homebrew, hacks with `--only-retail`, truly unknown dumps). Move them manually preserving the folder shape:

```sh
npx -y igir@latest \
  move \
  -i roms-unverified/ \
  -o roms-verified/ \
  --dir-mirror
```

This keeps the original subfolder structure but normalises extensions.

## Multi-disc reorganisation

Igir outputs multi-disc games as separate folders, which confuses multi-file game detection. Collapse them:

```sh
cd roms-verified/psx

ls -d *Disc* | while read file; do
    game=$(echo "${file}" | sed -E 's/ ?\(Disc.*//')
    mkdir -p "${game}"
    mv "${file}" "${game}"
    m3u="${game}/${game}.m3u"
    touch "${m3u}"
    echo "${file}" >> "${m3u}"
done
```

Before:

```text
Final Fantasy VII (Disc 1) (USA)/
Final Fantasy VII (Disc 2) (USA)/
Final Fantasy VII (Disc 3) (USA)/
```

After:

```text
Final Fantasy VII (USA)/
  Final Fantasy VII (Disc 1) (USA)/
  Final Fantasy VII (Disc 2) (USA)/
  Final Fantasy VII (Disc 3) (USA)/
  Final Fantasy VII (USA).m3u
```

The `.m3u` is a playlist RomM respects for launching multi-disc games.

## Importing

Once `roms-verified/` looks right, mount it as RomM's library:

```yaml
services:
    romm:
        volumes:
            - /path/to/roms-verified:/romm/library/roms:ro
```

Read-only is safer: if you need Igir to re-clean, work in a parallel folder and re-promote it to `roms-verified/`. Once you run a scan from RomM, and everything should match cleanly against providers!

## See also

- [Igir docs](https://igir.io/)
- [Folder Structure](../getting-started/folder-structure.md)
