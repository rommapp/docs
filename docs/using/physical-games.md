---
title: Physical Games
description: Track games you own on cartridge or disc, with no ROM file
---

# Physical Games

Own a game on a cartridge or disc but have no ROM for it? Add it anyway. A physical game is a library entry with no file behind it, and it gets the same metadata, artwork, collections, notes and ratings as everything else, so you're not keeping a separate list somewhere for the shelf.

Add one by name or by barcode. Either way RomM matches it against your enabled [metadata providers](../getting-started/metadata-providers.md) the same as it would a scanned file. You need the `roms.write` permission.

## Barcode lookup

A barcode gets sent to an external lookup service, which returns a product title, and that title is what the metadata providers then search for. Store listings are messy, so RomM trims them first: `Sonic - Nintendo Switch` becomes `Sonic`.

The lookup only produces a name. It doesn't attach any provider ids. If the barcode comes back with nothing usable, you get an error rather than an untitled entry, and you can add the game by name instead.

| Variable             | Default                                       | Purpose                                                  |
| -------------------- | --------------------------------------------- | -------------------------------------------------------- |
| `UPC_LOOKUP_ENABLED` | `true`                                        | Turn barcode lookups off entirely, leaving the name path |
| `UPC_LOOKUP_URL`     | `https://api.upcitemdb.com/prod/trial/lookup` | The lookup endpoint                                      |
| `UPC_LOOKUP_API_KEY` | _(unset)_                                     | Sent as the `user_key` header, for a plan that needs one |

Out of the box this hits [UPCitemdb](https://www.upcitemdb.com/)'s trial tier, which needs no account but is rate limited. Point `UPC_LOOKUP_URL` at their paid endpoint with a key if you hit the limit, or at anything else that answers `?upc=` with `{"items": [{"title": ...}]}`.

## What's different about them

No file means a few things work differently:

- They're **never flagged missing**, and the missing-ROM cleanup won't touch them.
- They **can't be downloaded or played**, and they're left out of the [gamelist.xml and Pegasus exports](../reference/exports.md) and the [device feeds](../ecosystem/feed-clients.md). Anything that needs a real file treats them the same as a missing one.
- They take up no space, and show as zero bytes in [server stats](../administration/server-stats.md).

You also get **one entry per title per platform**. Try to add the same game twice and RomM refuses, which is fine, because you can't own the same cartridge twice either. Under the hood the entries sit in a `.physical` folder that doesn't exist on disk and never gets scanned.

Everything else works as normal: [collections](collections.md), ratings, completion status, [walkthroughs](walkthroughs.md), manuals, and [RetroAchievements](retroachievements.md) for whatever it matched.

## Getting the ROM later

Just drop the file in the platform folder and scan. You'll end up with two entries, so delete the physical one once the real one has its metadata. There's no automatic merge.

## API

| Method | Path             | Description                                |
| ------ | ---------------- | ------------------------------------------ |
| `POST` | `/roms/physical` | Create a game with no file, by name or UPC |

Send a `platform_id` plus either a `name` or a `upc`. Add `metadata_sources` to limit which providers get asked, otherwise it uses all the enabled ones. The endpoint runs a quick scan inline and returns the matched game. If a provider blows up part way through, the entry is deleted rather than left behind half-populated.

Every ROM in `DetailedRomSchema` carries `is_physical`, `upc` and `has_file_on_disk`, which is enough to tell a physical game from a missing one from a normal one.

## Related

- [Metadata Providers](../getting-started/metadata-providers.md): what a physical game gets matched against
- [Collections](collections.md): shelving physical and digital copies together
- [Exports](../reference/exports.md): why file-less games are left out
