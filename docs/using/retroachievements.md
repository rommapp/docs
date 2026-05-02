---
title: RetroAchievements
description: Link your account to surface progression and browse unlocks
---

# RetroAchievements

[RetroAchievements](https://retroachievements.org/) adds achievements to retro games. Thousands of classic titles have had achievement sets authored by the community, from NES through PSX and beyond. When wired up to RetroAchievements, each user's progression (achievements unlocked, percentage complete, hardcore flag) is surfaced per-game.

<!-- prettier-ignore -->
!!! warning "Achievements can't be earned in the EmulatorJS player"
    The bundled in-browser player doesn't unlock achievements. RomM displays your existing progression synced from RetroAchievements, but new unlocks have to come from a RetroAchievements-capable standalone emulator.

## Linking your account

Enter your RetroAchievements username into your profile and hit Apply → Sync. Subsequent syncs run automatically through the nightly RetroAchievements Sync scheduled task (see [Scheduled Tasks](../administration/scheduled-tasks.md)), but on-demand syncs are also available.

## Hardcore mode

RetroAchievements distinguishes two play modes:

- **Softcore**: save states allowed
- **Hardcore**: more points per achievement but no saves allowed

Hardcore isn't enforced server-side, you toggle it per-game in RetroAchievements-capable cores. Loading a save state during a hardcore run will silently drop hardcore crediting on the RA server side, you'll still see the achievement but marked as softcore.

If you care about hardcore, use the in-game save feature instead of save states (see [Saves & States → RetroAchievements and states](saves-and-states.md#retroachievements-and-states)).

## Hash-based matching

Whether a ROM has RA support depends on the **hash** matching RA's database. Hash calculation runs as part of scans, so if you've disabled hashing (`filesystem.skip_hash_calculation: true`), you lose RA matching.

## Troubleshooting

- **Games don't show achievements**: ROM hash doesn't match RA's canonical. Try a No-Intro dump.
- **Achievements show 0/N but you've unlocked some**: initial sync hasn't run yet. Trigger an on-demand sync, or wait for the nightly.
- **Hardcore run didn't credit**: you probably loaded a save state mid-run. Start over and avoid states.

More in [Troubleshooting](../troubleshooting/index.md).
