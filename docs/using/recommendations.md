---
title: Recommendations
description: Similar games and a personalised feed, built from your own library
---

# Recommendations

RomM recommends games you already own, in two places:

- **Similar games**, on a game's page.
- **Recommended for you**, on the home screen.

Similar games used to be IGDB's list verbatim, which mostly named games you don't have and came up empty whenever IGDB hadn't matched the game at all. Both sections now rank your own library, and IGDB's list is just one of the inputs.

## How it works

A nightly task compares every game in your library against every other and stores the closest two dozen matches for each. Games score as similar when they share metadata. A shared collection or franchise counts for a lot, genres and themes and keywords for less, and platform and release decade barely at all.

How much a shared trait is worth depends on your library. If nine tenths of your games are platformers, "Platformer" tells RomM nothing and stops counting. You don't have to configure any of this.

**Recommended for you** re-ranks those matches against what you've been playing, at the moment you load the page rather than overnight, so a game you finished this morning already affects it. Ratings count in both directions: rate something below 5.5 and games like it get pushed down. Playtime counts with diminishing returns, and games you played recently count for more than ones you dropped a year ago.

Neither section will show you six Mega Man games in a row, and neither will surface a game or platform your account can't see.

Each recommendation comes with the reason it was picked, which is what the "why this was recommended" note shows.

## Building the index

**Build recommendations index** is the one [scheduled task](../administration/scheduled-tasks.md) that ships switched on. Both sections read the index, and with the task off they'd just sit empty.

It runs early each morning, after the nightly scan and metadata jobs have finished, and you can also run it by hand from the tasks page. In between runs, scans add new games to the index as they come in. Its schedule and enable variable are in [Environment Variables → Scans & Tasks](../reference/environment-variables.md#scans-tasks).

**Neither section appears until the index has been built once.** On a new instance, that's the morning after you set it up, or whenever you run the task yourself.

Users can hide either section in their own settings. To switch the feature off instance-wide, set `ENABLE_SCHEDULED_BUILD_RECOMMENDATIONS=false` and both sections stay empty, which also saves the nightly build on a very large library.

## API

| Method | Path                 | Description                             |
| ------ | -------------------- | --------------------------------------- |
| `GET`  | `/recommendations`   | The requester's recommended games       |
| `GET`  | `/roms/{id}/similar` | Library-aware similar games for one ROM |

`/recommendations` takes a `limit` (20 by default, 50 max) and a `refresh` flag to skip the cache. Every entry comes back with a score, its reasons, and the game that triggered it.

## Related

- [Collections](collections.md): the strongest signal the index reads
