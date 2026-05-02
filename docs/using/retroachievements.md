---
title: RetroAchievements
description: Link your RetroAchievements account, surface progression, and browse unlocks on your games.
---

# RetroAchievements

[RetroAchievements](https://retroachievements.org/) adds Xbox-style achievements to retro games. Thousands of classic titles have had achievement sets authored by the community, from NES through PSX and beyond.

When wired up to RetroAchievements, each user's progression (achievements unlocked, percentage complete, hardcore flag) is surfaced per-game.

## Prerequisites

1. **The operator** has to enable the provider (see [Metadata Providers → RetroAchievements](../administration/metadata-providers.md#retroachievements)).
2. **You** need a [RetroAchievements account](https://retroachievements.org/) and your personal API key from the [RA settings page](https://retroachievements.org/settings).

## Linking your account

Paste the username and API key into your profile and sync. Subsequent syncs run automatically through the nightly RetroAchievements Sync scheduled task (see [Scheduled Tasks](../administration/scheduled-tasks.md)). On-demand syncs are also available.

## Smart collections

[Smart collections](smart-collections.md) support a **Has Achievements** boolean field. Build "Games with achievements I haven't started" with a rule combining this + your Personal status.

## Hardcore mode

RetroAchievements distinguishes two play modes:

- **Softcore**: save states allowed. Achievements still count.
- **Hardcore**: no save states. More points per achievement, flagged separately

Hardcore isn't enforced server-side. You toggle it per-game in RetroAchievements-capable cores. Loading a save state during a hardcore run will silently drop hardcore crediting on the RA server side. You'll still see the achievement but marked as softcore.

If you care about hardcore, use the in-game save feature instead of save states (see [Saves & States → RetroAchievements and states](saves-and-states.md#retroachievements-and-states)).

## Supported platforms

Most 8/16-bit consoles and some later platforms: NES, SNES, Genesis, Game Boy family, PC Engine, Master System, Atari 2600/7800, N64, PlayStation, Saturn, Dreamcast, and more. Some platforms are hash-dependent, so your ROM has to match the RA canonical dump.

Full up-to-date list + hash requirements: [RA consoles + games](https://retroachievements.org/systemList.php).

## Hash-based matching

Whether a ROM has RA support depends on the **hash** matching RA's database. Hash calculation runs as part of scans, so if you've disabled hashing (`filesystem.skip_hash_calculation: true`), you lose RA matching.

Some tips:

- Prefer **No-Intro** / canonical dumps. Hacks, region-patched ROMs, or unusual dumps won't match.
- If a game you know has RA support shows no achievements, the hash is probably off. Try a different ROM source, or re-run a Hashes scan (see [Scanning & Watcher](../administration/scanning-and-watcher.md#scan-modes)).

## Privacy

- Your RA API key is stored server-side (per-user), encrypted at rest.
- Calls to RA only use your key for _your_ data, never shared across users.
- Admins can see which users have RA linked but not the API keys themselves.

## Troubleshooting

- **"Invalid API key"**: regenerate on the RA settings page, paste fresh.
- **Games don't show achievements**: ROM hash doesn't match RA's canonical. Try a No-Intro dump.
- **Achievements show 0/N but you've unlocked some**: initial sync hasn't run yet. Trigger an on-demand sync, or wait for the nightly.
- **Hardcore run didn't credit**: you probably loaded a save state mid-run. Start over and avoid states.

More in [Troubleshooting](../troubleshooting/index.md).

## API

```http
GET  /api/users/me/ra-progression    # your progression data
POST /api/users/me/ra/refresh        # trigger an on-demand sync
```

Requires `me.read` / `me.write`. Full API reference: [API Reference](../developers/api-reference.md).
