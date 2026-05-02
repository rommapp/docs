---
title: Smart Collections
description: Rule-based collections that auto-populate from your library
---

# Smart Collections

A **smart collection** is a collection defined by **filter criteria**, not by hand-picking. You set filters ("SNES games tagged RPG", "Zelda franchise", "playable in the browser") and RomM keeps the list in sync as you add ROMs and edit metadata.

For hand-curated collections, see [Collections](collections.md), and for auto-generated groupings, see [Virtual Collections](virtual-collections.md).

## How filters work

A smart collection holds a fixed set of filter fields (it isn't a generic rule engine). Each field accepts one or more values, and multi-value fields take a `<field>_logic` companion that picks `any` (OR) or `all` (AND) **within that field**. Different fields are always combined with **AND**.

That has three big consequences:

- **No top-level OR.** You can't express "Franchise = Zelda OR Title contains 'zelda'". Different fields always AND.
- **No negation.** Filters are inclusion-only. There's no "Status is not Complete" or "exclude Genre RPG". Pick the values you want, not the ones you don't.
- **No numeric thresholds.** No "Rating greater than 85" or "Playtime greater than 60 minutes". The age-rating filter is categorical (ESRB / PEGI labels), not a review-score number.

## Supported fields

- **Platform** (`platform_ids`): one or more platform slugs.
- **Genre** (`genres` + `genres_logic`): one or more genres, ANDed or ORed within the field.
- **Franchise** (`franchises`): one or more franchises.
- **Title** (`search_term`): case-insensitive substring match against the game title.
- **Status** (`statuses`): one or more personal play statuses (Never Played, Backlogged, Playing, Complete, Hidden). Inclusion only.
- **Age rating** (`age_ratings`): ESRB / PEGI categorical labels.
- **Playable in browser** (`playable`): boolean, restricts to platforms with an EmulatorJS or Ruffle core.

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

## Limitations

- **No top-level OR or nested groups.**
- **No numeric review-score or playtime thresholds.**
- **No nested smart collections**
