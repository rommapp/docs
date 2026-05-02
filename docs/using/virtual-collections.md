---
title: Virtual Collections
description: Auto-generated groupings by genre, developer, year, etc.
---

# Virtual Collections

**Virtual collections** are auto-generated collections that group ROMs by common metadata dimensions.

## What gets grouped

Virtual collections are generated for several dimensions:

| Dimension     | Example collections                                  |
| ------------- | ---------------------------------------------------- |
| **Genre**     | "Platformer", "RPG", "Shooter", "Puzzle", "Fighting" |
| **Developer** | "Nintendo EAD", "Capcom", "Konami", "id Software"    |
| **Publisher** | "Nintendo", "Sega", "Sony"                           |
| **Franchise** | "The Legend of Zelda", "Final Fantasy", "Mega Man"   |

Collections with too few ROMs are suppressed, so you won't see a "Developer: Some Indie Studio" with one entry.

## What you _can't_ do

Virtual collections are read-only, so you can't:

- Add a ROM by hand (use a [standard collection](collections.md))
- Remove a ROM (its metadata determines membership)
- Make one "public" vs "private" (they're always visible)
- Rename them (they take their name from the metadata dimension)
- Set a custom cover image

## "Why isn't my game in [X]?"

A game missing from "Virtual Collection: RPG" probably doesn't have the `RPG` genre set on its metadata. Either manually edit the genre, run an Unmatche scan, or add it to the collection by hand with a standard collection.
