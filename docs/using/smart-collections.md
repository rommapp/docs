---
title: Smart Collections
description: Rule-based collections that auto-populate from your library, new in 5.0.
---

# Smart Collections

A **smart collection** is a collection defined by **rules**, not by hand-picking. You describe what's in it ("all SNES games rated ≥4 stars", "everything in the Zelda franchise", "games I've beaten"), and RomM keeps the list in sync automatically: as you add ROMs, update ratings, mark games complete, the collection updates.

New in 5.0. For hand-curated collections, see [Collections](collections.md). For auto-generated-by-RomM groupings, see [Virtual Collections](virtual-collections.md).

## Creating a smart collection

1. **Collections** drawer → **+ New Smart Collection**.
2. Name it.
3. Build the rule set by adding one or more **conditions**.
4. Save.

The collection is live immediately: populated with every ROM currently matching the rules, and updated on every relevant change afterward.

## Rule structure

A smart collection is one or more **conditions** joined by **all** (AND) or **any** (OR).

Each condition has three parts:

1. **Field**: what you're matching on.
2. **Operator**: comparison (equals, contains, greater-than, etc.).
3. **Value**: the thing you're comparing against.

## Supported fields

### Metadata

- **Platform**: platform slug.
- **Title**: game title (case-insensitive substring match with `contains`).
- **Genre**: IGDB genre tag.
- **Franchise**: game franchise (Mario, Final Fantasy, etc.).
- **Developer**: company that made the game.
- **Publisher**: company that released it.
- **Release Year**: year.
- **Age Rating**: ESRB / PEGI rating.
- **Region**: game region (USA, Japan, Europe, World, etc.).
- **Language**: game language.
- **Rating**: IGDB / ScreenScraper critic score.

### Personal data

- **Personal Rating**: your per-game rating.
- **Status**: Never Played / Backlogged / Playing / Complete / Hidden.
- **Playtime**: accumulated play time (minutes).
- **Favourites**: whether you've favourited it.
- **Has Achievements**: whether the game has [RetroAchievements](retroachievements.md).

### Flags

- **Matched**: has a provider ID.
- **Playable in browser**: supports EmulatorJS / Ruffle.
- **Has Firmware**: required firmware exists in the library.
- **Duplicate**: the same game appears twice.

## Operators

Available operators depend on the field type:

| Operator                               | Works with                                           |
| -------------------------------------- | ---------------------------------------------------- |
| `equals`, `not equals`                 | Everything.                                          |
| `contains`, `does not contain`         | Text fields.                                         |
| `starts with`, `ends with`             | Text fields.                                         |
| `is`, `is not`                         | Boolean / enum fields (Status, Matched, Favourites). |
| `greater than`, `less than`, `between` | Numeric fields (Rating, Playtime, Release Year).     |
| `in`, `not in`                         | Multi-value fields (Region, Language, Genre).        |

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

(Combine `all of` + `any of` by nesting. The rule editor supports groups.)

## Public / private

Same visibility model as standard collections:

- **Private**: only you see it (your personal data fields matter).
- **Public**: everyone on the instance sees it. _Your_ personal-data rules still apply. If your smart collection is "games I haven't finished", every user sees _your_ unfinished games.

For shared rule sets across users, use metadata-only fields and keep the collection public. Rules that reference Personal data (status, rating, playtime, favourites) only make sense as private collections.

## Refresh behaviour

Smart collections refresh:

- **Live**: when you add, remove, rate, or edit a ROM, RomM re-evaluates rules instantly.
- **On scan**: after every scan, rules are re-evaluated against the new state.
- **No manual refresh needed** but admins can trigger a full re-evaluation via **Administration → Tasks → Refresh Smart Collections** if something looks stale.

## Editing a rule

Open the smart collection → drawer → **Edit**. The rule builder reopens with current rules pre-loaded. Save, and the collection updates immediately.

## Deleting

Same as standard collections: removes the definition. ROMs stay in the library.

## Limitations

- **No nested smart collections**: a smart collection can't reference another collection as a source. Compose rules directly.
- **Performance**: very complex rule sets (many conditions, many nested groups) on huge libraries can slow down the gallery load. Usually imperceptible but mentioned here for completeness.
- **Timezone**: "Release Year" uses UTC, not the user's timezone. Edge-case edge-of-year games might fall on the "wrong" side.

## API

```http
POST   /api/collections/smart           # create
GET    /api/collections/smart           # list
GET    /api/collections/smart/{id}      # get
PUT    /api/collections/smart/{id}      # update
DELETE /api/collections/smart/{id}      # delete
```

Rule schema is part of the POST body. See the [API Reference](../developers/api-reference.md) for the JSON structure. Requires `collections.read` / `collections.write`.
