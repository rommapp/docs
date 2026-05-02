---
title: Smart Collections
description: Rule-based collections that auto-populate from your library
---

# Smart Collections

A **smart collection** is a collection defined by **filter rules**. You describe what's in it (like "all SNES games rated ≥4 stars"), and the list stays in sync. The collection updates itself as you add ROMs to your library, update ratings, and manually match games.

For hand-curated collections, see [Collections](collections.md), and for auto-generated groupings, see [Virtual Collections](virtual-collections.md).

## Rule structure

A smart collection is one or more **conditions** joined by **all** (AND) or **any** (OR).

Each condition has three parts:

1. **Field**: what you're matching on
2. **Operator**: comparison (equals, contains, greater-than, etc.)
3. **Value**: the thing you're comparing against

## Supported fields

### Metadata

- **Platform**: platform slug
- **Title**: game title (case-insensitive substring match with `contains`)
- **Genre**: IGDB genre tag
- **Franchise**: game franchise (Mario, Final Fantasy, etc.)
- **Developer**: company that made the game
- **Publisher**: company that released it
- **Release Year**: year
- **Age Rating**: ESRB/PEGI rating
- **Region**: game region (USA, Japan, Europe, World, etc.)
- **Language**: game language
- **Rating**: IGDB/ScreenScraper critic score

### Personal data

- **Personal Rating**: your per-game rating
- **Status**: Never Played/Backlogged/Playing/Complete/Hidden
- **Playtime**: accumulated play time (minutes)
- **Favourites**: whether you've favourited it
- **Has Achievements**: whether the game has [RetroAchievements](retroachievements.md)

### Flags

- **Matched**: has a provider ID
- **Playable in browser**: supports EmulatorJS/Ruffle
- **Has Firmware**: required firmware exists in the library.
- **Duplicate**: the same game appears twice.

## Operators

Available operators depend on the field type:

| Operator                               | Works with                                         |
| -------------------------------------- | -------------------------------------------------- |
| `equals`, `not equals`                 | Everything.                                        |
| `contains`, `does not contain`         | Text fields.                                       |
| `starts with`, `ends with`             | Text fields.                                       |
| `is`, `is not`                         | Boolean/enum fields (Status, Matched, Favourites). |
| `greater than`, `less than`, `between` | Numeric fields (Rating, Playtime, Release Year).   |
| `in`, `not in`                         | Multi-value fields (Region, Language, Genre).      |

## Examples

### "SNES RPGs I haven't finished"

```text
all of:
  - Platform equals "snes"
  - Genre in ["RPG"]
  - Status is not "Complete"
```

### "Top-rated arcade games that run in browser"

```text
all of:
  - Platform equals "arcade"
  - Rating greater than 85
  - Playable in browser is "yes"
```

### "Everything I've touched recently but not finished"

```text
all of:
  - Playtime greater than 60
  - Status is not "Complete"
```

### "Zelda franchise, any platform"

```text
any of:
  - Franchise equals "The Legend of Zelda"
  - Title contains "zelda"
```

## Public/private

Same visibility model as standard collections:

- **Private**: only you see it (your personal data fields matter).
- **Public**: everyone on the instance sees it, but _your_ personal-data rules still apply.

For shared rule sets across users, use metadata-only fields and keep the collection public. Rules that reference Personal data (status, rating, playtime, favourites) only make sense as private collections.

## Refresh behaviour

Smart collections refresh themselves when you add, remove, rate, or edit a ROM, so the list is always up to date. No manual refresh needed!

## Limitations

- **No nested smart collections**: a smart collection can't reference another collection as a source.
- **Performance**: very complex rule sets (many conditions, many nested groups) on huge libraries can slow down the gallery load.
