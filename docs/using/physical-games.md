---
title: Physical Games
description: Track games you own on cartridge or disc
---

# Physical Games

Own a game on a cartridge or disc but have no ROM for it? Add it anyway! A physical game is a library entry with no file behind it, and it gets the same metadata, artwork, collections, notes and ratings as everything else, so you're not keeping a separate list somewhere for the shelf.

Add one by name or by barcode, and it gets matched against your enabled [metadata providers](../getting-started/metadata-providers.md) the same as it would a scanned file.

## Barcode lookup

A barcode gets sent to an external lookup service, which returns a product title, and that title is what the metadata providers use to search. If the barcode comes back with nothing usable, you get an error rather than an untitled entry, and you can add the game by name instead.

By default, we use [UPCitemdb](https://www.upcitemdb.com/)'s trial tier, which needs no account but is rate limited. If you hit the limit, point `UPC_LOOKUP_URL` at their paid endpoint and set `UPC_LOOKUP_API_KEY` in your env vars, or point it at anything else that answers `?upc=` with `{"items": [{"title": ...}]}`. `UPC_LOOKUP_ENABLED=false` turns barcode lookups off entirely and leaves you the name path.

Defaults for all three are in [Environment Variables → Physical Games](../reference/environment-variables.md#physical-games).

## What's different about them

No file means a few things work differently:

- They're **never flagged missing**, and the missing-ROM cleanup won't touch them.
- They **can't be downloaded or played**, and they're left out of the [gamelist.xml and Pegasus exports](../reference/exports.md) and the [device feeds](../ecosystem/feed-clients.md). Anything that needs a real file treats them the same as a missing one.
- They take up no space, and show as zero bytes in [server stats](../administration/server-stats.md).

Everything else works as normal: [collections](collections.md), ratings, completion status, [walkthroughs](walkthroughs.md), manuals, and [RetroAchievements](retroachievements.md) for whatever it matched.

If you dump the ROM in the future, drop the file in the platform folder and scan. There's no automatic merge and you'll end up with two entries, so delete the physical one once the real one has its metadata.

## API

| Method | Path             | Description                                |
| ------ | ---------------- | ------------------------------------------ |
| `POST` | `/roms/physical` | Create a game with no file, by name or UPC |

Send a `platform_id` plus either a `name` or a `upc`. Add `metadata_sources` to limit which providers get asked, otherwise it uses all the enabled ones. The endpoint runs a quick scan inline and returns the matched game.

Every ROM in `DetailedRomSchema` carries `is_physical`, `upc` and `has_file_on_disk`, which is enough to tell a physical game from a missing one from a normal one.
