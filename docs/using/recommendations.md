---
title: Recommendations
description: Similar games and a personalised feed, built from your own library
---

# Recommendations

RomM recommends games from **your library**, on two surfaces:

- **Similar games** on a game's page, the closest games you own to the one you are looking at.
- **Recommended for you** on the home screen, ranked against what you actually play.

Similar games used to come straight from IGDB, which mostly named games you don't own and returned nothing at all when IGDB never matched the game in the first place. Both surfaces now rank your own shelf, with IGDB's list folded in as one signal among several.

## How it works

A scheduled task builds an **item-item similarity graph** over the library, keeping the closest two dozen neighbours per game. Two games are close when they overlap on facets: shared collections and franchises pull hardest, then genres, perspectives, themes, keywords and developers, with publishers, game modes, platform and decade counting as context rather than taste. IGDB's own similar-games list and a high rating each add an edge of their own.

The weighting is **library-relative**. A facet counts for as much as it is rare _in your library_, so a shelf that is nine-tenths platformers doesn't have "Platformer" tell it anything, and no shelf needs its weights tuned by hand.

The personalised feed is ranked **on demand** from that graph plus live activity, rather than precomputed per user. A game you played an hour ago is exactly the signal that matters most, and a nightly feed would ignore it. Your ratings steer it in both directions, since anything below the middle of the 1-10 scale pushes similar games away rather than merely not pulling them in. Playtime saturates, because the gap between one hour and ten says a great deal and the gap between a hundred and two hundred says almost nothing, and older play counts for less on a roughly two-month half-life without dropping out entirely.

Both surfaces cap how many games one series may contribute, so a deep franchise can't fill the whole row, and both respect visibility, so a recommendation never names a platform or game the viewer can't see.

Every recommendation carries its reasons, which is what the "why this was recommended" explanation reads: the facets the two games share, or that it came from IGDB's list, or that it is simply highly rated.

## Building the index

| Variable                                 | Default      | Purpose             |
| ---------------------------------------- | ------------ | ------------------- |
| `ENABLE_SCHEDULED_BUILD_RECOMMENDATIONS` | `true`       | The nightly rebuild |
| `SCHEDULED_BUILD_RECOMMENDATIONS_CRON`   | `30 5 * * *` | When it runs        |

This one is **on by default**, unlike the other [scheduled tasks](../administration/scheduled-tasks.md), because the index is what both surfaces read and leaving it off silently empties them. It runs after the nightly scan and metadata tasks so it builds against a settled library, and it can also be run by hand from the tasks page. Scans top the graph up incrementally in between, so newly added games don't wait for the next full build to appear.

Both sections stay hidden until the index has been built at least once. On a fresh instance that means after the first nightly run, or after running the task by hand.

A full build derives the whole graph from one consistent snapshot of the library, since the weighting shifts as the shelf grows.

## Turning them off

Each user can hide either surface from their own settings, without affecting anyone else or stopping the index from being built.

To switch the feature off for the whole instance, set `ENABLE_SCHEDULED_BUILD_RECOMMENDATIONS=false`. The index stops being rebuilt and both sections stay empty, which also saves the nightly build on a large library.

## API

| Method | Path                 | Description                             |
| ------ | -------------------- | --------------------------------------- |
| `GET`  | `/recommendations`   | The requester's recommended games       |
| `GET`  | `/roms/{id}/similar` | Library-aware similar games for one ROM |

`/recommendations` takes a `limit` (up to 50, 20 by default) and a `refresh` flag that bypasses the cached ranking. Each entry carries a score, the reasons behind it, and the game in your library that seeded it.

## Related

- [Scheduled Tasks](../administration/scheduled-tasks.md): the nightly build alongside the rest
- [Collections](collections.md): the strongest signal the index reads
