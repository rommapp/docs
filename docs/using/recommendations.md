---
title: Recommendations
description: Similar games and a personalised feed built from your library
---

# Recommendations

RomM recommends games you already own in two places:

- **Similar games**, on a game's page.
- **Recommended for you**, on the home screen.

## How it works

A nightly task compares every game in your library against every other and stores the closest two dozen matches for each. Games score as similar when they share metadata. A shared collection or franchise counts for a lot, genres, themes and keywords for less, and platform and release decade very little.

You don't have to configure any of this. How much a shared trait is worth depends on your library. If nine tenths of your games are platformers, "Platformer" tells us nothing and stops counting.

**Recommended for you** re-ranks those matches against what you've been playing, at the moment you load the page rather than overnight, so a game you finished this morning already affects it. Ratings count in both directions: rate something below 5.5 and games like it get pushed down. Playtime counts with diminishing returns, and games you played recently count for more than ones you dropped a year ago.

## Building the index

**Build recommendations index** is the only [scheduled task](../administration/scheduled-tasks.md) that's enabled by default. It runs early each morning, after the nightly scan and metadata jobs have finished, and you can run it by hand from the tasks page. In between runs, scans add new games to the index as they come in. Its schedule and enable variable are in [Environment Variables → Scans & Tasks](../reference/environment-variables.md#scans-tasks).

**Similar games** stays empty until the index has been built once, which on a new instance is the morning after you set it up, or whenever you run the task yourself. **Recommended for you** doesn't wait: with no index and nothing played yet, it falls back to the best-reviewed games in your own library.

Users can hide either section in their own settings. Setting `ENABLE_SCHEDULED_BUILD_RECOMMENDATIONS=false` only stops the nightly rebuild, which saves the work on a very large library; both sections stay visible.

## API

| Method | Path                 | Description                             |
| ------ | -------------------- | --------------------------------------- |
| `GET`  | `/recommendations`   | The requester's recommended games       |
| `GET`  | `/roms/{id}/similar` | Library-aware similar games for one ROM |

`/recommendations` takes a `limit` (20 by default, 50 max) and a `refresh` flag to skip the cache. Every entry comes back with a score, its reasons, and the game that triggered it.

## Related

- [Collections](collections.md): the strongest signal the index reads
