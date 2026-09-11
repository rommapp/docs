---
title: Physical Games
description: Track games you own on cartridge or disc, with no ROM file
---

# Physical Games

A physical game is a library entry for a copy you own on a cartridge or a disc but have no ROM file for. It carries the same metadata, artwork, collections, notes and ratings as any other game, so your shelf and your library are one list instead of two.

You add one by name, or by its barcode, and RomM matches it against your enabled [metadata providers](../getting-started/metadata-providers.md) exactly as a scanned file would be. Adding one needs the `roms.write` permission.

## Barcode lookup

Scanning a barcode resolves the UPC or EAN to a product title through an external lookup service, and that title is what gets matched against the metadata providers. RomM strips the retail noise those catalogues carry (`Sonic - Nintendo Switch` becomes `Sonic`) before searching, since a store listing's title is rarely the title a game database knows.

The lookup attaches no provider ids of its own, it only produces a name. A barcode that resolves to nothing usable is rejected rather than creating a nameless entry, so you can fall back to adding the game by name.

| Variable             | Default                                       | Purpose                                                  |
| -------------------- | --------------------------------------------- | -------------------------------------------------------- |
| `UPC_LOOKUP_ENABLED` | `true`                                        | Turn barcode lookups off entirely, leaving the name path |
| `UPC_LOOKUP_URL`     | `https://api.upcitemdb.com/prod/trial/lookup` | The lookup endpoint                                      |
| `UPC_LOOKUP_API_KEY` | _(unset)_                                     | Sent as the `user_key` header, for a plan that needs one |

The default endpoint is [UPCitemdb](https://www.upcitemdb.com/)'s trial tier, which is rate limited and needs no account. Point `UPC_LOOKUP_URL` at their paid endpoint with a key, or at any service that answers `?upc=` with the same `{"items": [{"title": ...}]}` shape.

## What a physical game is not

A physical entry has no file behind it, which changes what RomM will do with it:

- It is **never flagged missing from the filesystem** and is never removed by the missing-ROM cleanup, since there was never a file to lose.
- It is **excluded from downloads and playback**, and from the [gamelist.xml and Pegasus exports](../reference/exports.md) and the [device feeds](../ecosystem/feed-clients.md), all of which need a real file. RomM treats "physical" and "missing" alike wherever a file is required.
- It does **not** occupy space, and reports a size of zero in [server stats](../administration/server-stats.md).

Entries live under a sentinel `.physical` folder inside the platform's ROM folder. That folder never exists on disk and is never scanned, it just gives the entry a path to be unique within. One consequence is that a platform holds **one entry per title**: adding the same game twice is rejected, which matches what you can actually own.

Everything else behaves normally. A physical game can join [collections](collections.md), be rated and marked completed, carry [walkthroughs](walkthroughs.md) and manuals, and show [RetroAchievements](retroachievements.md) for the matched game.

## Getting the ROM later

Nothing special is needed. Drop the file into the platform folder, scan, and you have both entries. Merging them is a manual step, so delete the physical entry once the scanned one has picked up the metadata you want.

## API

| Method | Path             | Description                                |
| ------ | ---------------- | ------------------------------------------ |
| `POST` | `/roms/physical` | Create a game with no file, by name or UPC |

The request takes a `platform_id` and either a `name` or a `upc`, plus an optional `metadata_sources` list to narrow which providers are consulted (all enabled ones by default). It runs a single quick scan inline and returns the matched game, so a provider failure rolls the entry back rather than leaving a metadata-less row behind.

`DetailedRomSchema` carries `is_physical`, `upc` and `has_file_on_disk` for every ROM, so a client can tell the three states apart.

## Related

- [Metadata Providers](../getting-started/metadata-providers.md): what a physical game gets matched against
- [Collections](collections.md): shelving physical and digital copies together
- [Exports](../reference/exports.md): why file-less games are left out
