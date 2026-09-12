---
title: Smart Collections
description: Rule-based collections that auto-populate from your library
---

# Smart Collections

A **smart collection** is a collection defined by **filter criteria**, not by hand-picking. You set filters ("SNES games tagged RPG", "Zelda franchise", "playable in the browser") and RomM keeps the list in sync as you add ROMs and edit metadata.

For hand-curated collections, see [Collections](collections.md), and for auto-generated groupings, see [Virtual Collections](virtual-collections.md).

## How filters work

A smart collection holds a fixed set of filter fields (it isn't a generic rule engine). Each field accepts one or more values, and multi-value fields take a `<field>_logic` companion that picks `any` (OR) or `all` (AND) **within that field**. Different fields are always combined with **AND**.

That has two big consequences:

- **No top-level OR.** You can't express "Franchise = Zelda OR Title contains 'zelda'". Different fields always AND.
- **No negation.** Filters are inclusion-only. There's no "Status is not Complete" or "exclude Genre RPG". Pick the values you want, not the ones you don't.
- **No nesting.** A smart collection can't filter on another smart collection.

## Supported fields

### Multi-value

Each takes one or more values. All (except `platform_ids`) also accept a `<field>_logic` companion of `any` (OR, the default) or `all` (AND).

| Field                | Matches                                      |
| -------------------- | -------------------------------------------- |
| `platform_ids`       | One or more platforms                        |
| `genres`             | Game genres                                  |
| `franchises`         | Franchises                                   |
| `collections`        | Membership in named collections              |
| `companies`          | The combined company credit                  |
| `publishers`         | Publishers specifically                      |
| `developers`         | Developers specifically                      |
| `age_ratings`        | ESRB / PEGI categorical labels               |
| `regions`            | Region tags                                  |
| `languages`          | Language tags                                |
| `tags`               | Arbitrary filename tags                      |
| `statuses`           | Your play status (backlogged, playing, etc.) |
| `player_counts`      | Supported player counts                      |
| `metadata_providers` | Which provider matched the game              |

### Boolean

| Field            | Matches                                                           |
| ---------------- | ----------------------------------------------------------------- |
| `matched`        | Games a metadata provider matched                                 |
| `verified`       | Games with a verified match                                       |
| `favorite`       | Your favourites                                                   |
| `duplicate`      | Games with more than one version                                  |
| `playable`       | Platforms with a browser player                                   |
| `has_ra`         | Games with a [RetroAchievements](retroachievements.md) set        |
| `has_saves`      | Games you have a save for                                         |
| `has_states`     | Games you have a state for                                        |
| `has_soundtrack` | Games with tracks in the [Jukebox](jukebox.md)                    |
| `missing`        | Games flagged missing from the filesystem                         |
| `physical`       | [Physical games](physical-games.md), entries with no file on disk |

### Single-value

| Field                                        | Matches                                            |
| -------------------------------------------- | -------------------------------------------------- |
| `search_term`                                | Case-insensitive substring match against the title |
| `collection_id`, `virtual_collection_id`     | Membership in one specific collection              |
| `hltb_main_story_min`, `hltb_main_story_max` | A [game length](#game-length) range                |

## Game length

Lengths come from [HowLongToBeat](../getting-started/metadata-providers.md#howlongtobeat), so you need `HLTB_API_ENABLED=true` and a scan that matched the game. It's **main story** time, and you can set a floor, a ceiling, or both. The gallery sorts and filters by it too, without needing a collection. Games HowLongToBeat never matched have no length at all and drop out of a length filter entirely.

## Examples

### "SNES RPGs I'm playing or haven't started"

```text
Platform: snes
Genre: RPG
Status: Never Played, Playing
```

Inclusion-only, so list the statuses you want and let everything else fall away.

### "Arcade games playable in browser"

```text
Platform: arcade
Playable in browser: yes
```

### "Short games I own physically and haven't started"

```text
Physical: yes
Status: Never Played
Main story: up to 8 hours
```

### "Zelda franchise"

```text
Franchise: The Legend of Zelda
```

To match by title substring instead, use `Title: zelda`. You can't OR the two together in one collection (different fields always AND).

## Public / private

Same visibility model as standard collections:

- **Private**: only you see it. Personal-data fields (Status) only make sense here.
- **Public**: everyone on the instance sees it. _Your_ personal-data filters still apply, so a public smart collection filtering on Status will reflect _your_ statuses for every viewer.

## Refresh behaviour

Smart collections refresh on add/remove/edit of ROMs, and on scan. No manual refresh needed!
