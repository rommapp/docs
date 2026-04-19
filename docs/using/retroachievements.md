---
title: RetroAchievements
description: Link your RetroAchievements account, surface progression, and browse unlocks on your games.
---

# RetroAchievements

[RetroAchievements](https://retroachievements.org/) adds Xbox-style achievements to retro games. Thousands of classic titles have had achievement sets authored by the community, from NES through PSX and beyond.

When RomM is wired up to RetroAchievements, each user's progression (achievements unlocked, percentage complete, hardcore flag) is surfaced per-game in the UI.

## Prerequisites

1. **RomM operator** has to enable the provider. See [Metadata Providers → RetroAchievements](../administration/metadata-providers.md#retroachievements). Check by looking for the achievement tab on any known-supported game. If it's absent, the provider isn't active.
2. **You** need a [RetroAchievements account](https://retroachievements.org/) and your personal **API key**.

## Linking your account

1. Go to your [RA settings page](https://retroachievements.org/settings).
2. Scroll to **Web API Keys** → copy the generated key.
3. In RomM → **Profile** → **RetroAchievements** section → paste:
    - **Username**: your RA username (case-sensitive).
    - **API Key**: the key you just copied.
4. **Sync now**: RomM pulls your progression data and populates the Achievements tab on matched games.

From this point on, RomM auto-syncs every user's progression via the nightly RetroAchievements Sync scheduled task. See [Scheduled Tasks](../administration/scheduled-tasks.md). No manual sync needed but you can force one from the Profile page whenever.

## Where it shows up

### Game detail → Achievements tab

Per-game breakdown:

- Total achievements authored.
- How many you've unlocked.
- Points earned / total points available.
- Hardcore vs softcore totals (if applicable).
- List of specific achievements with icons and descriptions.

### Game cards

A small badge appears on games where RA achievements exist, regardless of whether you've unlocked any yet. Hover for percentage complete.

### Filters

- **Show RetroAchievements**: filter to games that have RA achievements.
- You can combine with **Show Unmatched** or **Status: Playing** to find targets.

### Smart collections

[Smart collections](smart-collections.md) support a **Has Achievements** boolean field. Build "Games with achievements I haven't started" with a rule combining this + your Personal status.

## Hardcore mode

RetroAchievements distinguishes two play modes:

- **Softcore**: save states allowed. Achievements still count.
- **Hardcore**: no save states. More points per achievement, flagged separately.

RomM doesn't enforce hardcore. You toggle it per-game in RetroAchievements-capable cores. Loading a save state during a hardcore run will silently drop hardcore crediting on the RA server side. You'll still see the achievement but marked as softcore.

If you care about hardcore, use the in-game save feature instead of save states. See [Saves & States → RetroAchievements and states](saves-and-states.md#retroachievements-and-states).

## Supported platforms

Most 8/16-bit consoles and some later platforms: NES, SNES, Genesis, Game Boy family, PC Engine, Master System, Atari 2600/7800, N64, PlayStation, Saturn, Dreamcast, and more. Some platforms are hash-dependent, so your ROM has to match the RA canonical dump.

Full up-to-date list + hash requirements: [RA consoles + games](https://retroachievements.org/systemList.php).

## Hash-based matching

Whether a ROM has RA support depends on the **hash** matching RA's database. Hash calculation runs as part of scans, so if you've disabled hashing (`filesystem.skip_hash_calculation: true`), you lose RA matching.

Some tips:

- Prefer **No-Intro** / canonical dumps. Hacks, region-patched ROMs, or unusual dumps won't match.
- If a game you know has RA support shows no achievements, the hash is probably off. Try a different ROM source, or re-run a Hashes scan. See [Scanning & Watcher](../administration/scanning-and-watcher.md#scan-modes).

## Privacy

- Your RA API key is stored server-side (per-user), encrypted at rest.
- RomM only calls RA using your key for _your_ data, never shares across users.
- Admins can see which users have RA linked but not the API keys themselves.

To unlink: Profile → RetroAchievements → **Unlink** → confirm. Key is deleted. Progression data stays cached until the next sync pass.

## Troubleshooting

- **"Invalid API key"**: regenerate on the RA settings page, paste fresh.
- **Games don't show the Achievements tab**: ROM hash doesn't match RA's canonical. Try a No-Intro dump.
- **Achievements show 0/N but you've unlocked some**: initial sync hasn't run yet. Click **Sync now** on your Profile page, or wait for the nightly.
- **Hardcore run didn't credit**: you probably loaded a save state mid-run. Start over and avoid states.

More in [Troubleshooting](../troubleshooting/index.md).

## API

```http
GET  /api/users/me/ra-progression    # your progression data
POST /api/users/me/ra/refresh        # trigger an on-demand sync
```

Requires `me.read` / `me.write`. Full API reference: [API Reference](../developers/api-reference.md).
