<!-- trunk-ignore-all(markdownlint/MD041) -->

[Igir](https://igir.io/) is a zero-setup ROM collection manager that sorts, filters, extracts or archives, patches, and reports on collections of any size on any OS. It can be used to rename your ROMs to match the RomM database, and to move them into a new directory structure.

## Setup

### Directory structure

The directory structure is important for running the bulk ROM renaming script. Before running the bulk ROM renaming script, set up your directories as follows:

```md
.
├── dats/ # DAT files from no-intro.org
├── roms/ # Original ROM collection
├── roms-unverified/ # Working copy of ROMs
└── igir-romm-cleanup.sh
```

### Initial Setup Steps

1. Create a working copy of your ROMs:

    ```bash
    cp -r roms/ roms-unverified/
    ```

    This provides a safe working environment and allows for easy script adjustment if needed.

2. Download DAT Files:

    - For cartridge-based systems:
        - Visit [No-Intro.org Daily Download](https://datomatic.no-intro.org/index.php?page=download&op=daily)
        - Download the latest DAT compilation
    - For optical media (e.g., PlayStation):
        - Visit [redump.org](http://redump.org/downloads/)
        - Download platform-specific DAT files

    Extract the DAT files to your `dats` directory. You can optionally extract a subset of the .dat files into the directory instead.

## Configuration

Create the cleanup script `igir-romm-cleanup.sh` with the contents below:

```bash
#!/usr/bin/env bash
set -ou pipefail
cd "$(dirname "${0}")"

INPUT_DIR=roms-unverified
OUTPUT_DIR=roms-verified

# Documentation: https://igir.io/
# Uses dat files: https://datomatic.no-intro.org/index.php?page=download&op=daily
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

Make the script executable:

```bash
chmod a+x igir-romm-cleanup.sh
```

## Usage

### Run the script

Run the script. It will generate a new output directory named `roms-verified`, moving the files from `roms-unverified` if its checksum matches any of the known checksums in the DAT files provided. Any ROMs not identified will remain in the `roms-unverified` directory.

### Manually move over remaining files

The script may not identify all of the ROMs in your input directory. You can choose to migrate them over manually:

```bash
npx -y igir@latest \
  move \
  -i roms-unverified/ \
  -o roms-verified/ \
  --dir-mirror
```

This will move your ROMs from the input to the output directory, preserving the subdirectory structure. It also cleans up file extensions in the process.

### Reorganize multi-disc games

The Igir script will move games that have multiple discs to separate folders. This can confuse RomM's game detection, and those games need to be reorganized into single folders with many discs.

To do this enter your platform directory, such as `ps` or `psx` and run the following:

```bash
ls -d Disc | while read file; do
    game=$(echo "${file}" | sed -E 's/ ?(Disc.*//')
    mkdir -p "${game}"
    mv "${file}" "${game}"
    m3u="${game}/${game}.m3u"
    touch "${m3u}"
    echo "${file}" >> "${m3u}"
done
```

This will find any directory with `(Disc` in the name and move the files into a new directory without the `(Disc #)` string. For example:

Before:

```bash
Final Fantasy VII (Disc 1) (USA)
Final Fantasy VII (Disc 2) (USA)
```

Gets combined to:

```bash
Final Fantasy VII (USA)
```
