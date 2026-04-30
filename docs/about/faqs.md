---
title: FAQs
description: Answers to the questions users most often ask about RomM.
---

# FAQs

## What is RomM?

A self-hosted ROM manager + player: scan your library, pull metadata, browse a clean UI, play in the browser, sync to handhelds, and run it all on your own hardware.

See [Introduction](../index.md) for the full pitch, or [Quick Start](../getting-started/quick-start.md) to stand one up.

<!-- prettier-ignore -->
!!! note "RomM is server software you run on a homelab box or NAS"
    It is not a desktop app, and there's no `.exe` or `.appimage`. You'll need basic Linux + Docker skills to set it up. Games and copyrighted material aren't provided.

## Is it free?

Yes! Licensed under [AGPL-3.0](license.md), the core will always be free. Other repos under our umbrella use equally permissive licenses, and there's no tracking or upsells.

## How does it compare to [X other manager]?

The emphasis here is self-hosted + multi-user + in-browser-play + the companion-app ecosystem. If those matter, try it, but if you just want a local Windows app that scans a folder, tools like LaunchBox may fit better.

## Do I need metadata API keys?

Not strictly. It runs without any but games won't match against a metadata source, so no covers, descriptions, or ratings.

Hasheous + IGDB + SteamGridDB + RetroAchievements is the recommended set, though many users only run ScreenScraper + Retroachievements (see [Metadata Providers](../administration/metadata-providers.md) for the full list).

## Is RomM legal?

The software is legal but what you put in it depends on your jurisdiction. **We don't ship ROMs or firmware, don't help you find them, and can't give legal advice.**

## Can I run RomM on [X]?

Probably! Supported deployment paths:

- Docker Compose (Linux, macOS, Windows with WSL2)
- Unraid / Synology / TrueNAS SCALE
- Kubernetes

See [Install & Deploy](../install/index.md).

Not supported:

- Bare metal without containers (undocumented but _should_ work)
- TrueNAS CORE (FreeBSD)
- Windows without WSL

## How much RAM / CPU does it need?

- **Minimum** (small library, 1 user): 512 MB RAM, any modest CPU
- **Comfortable** (thousands of ROMs, a few users, occasional scans): 2 GB RAM, 2 cores

Heaviest CPU usage is during scans, as hashing and network-bound metadata calls may cause spikes.

## How do I update?

```sh
docker compose pull rommapp/romm
docker compose up -d romm
```

Always [read the release notes](../releases/index.md) before minor or major version upgrades!

## Why can't I see a specific platform?

The platform folder name probably doesn't match a known slug. Check [Supported Platforms](../platforms/supported-platforms.md), and fix it by either renaming the folder or updating the [`system.platforms`](../reference/configuration-file.md#systemplatforms) binding in `config.yml`.

## Why are my ROMs unmatched after a scan?

Most common reasons:

- No metadata providers configured
- Filename too generic (no tags, unusual naming)
- Wrong platform detection

Full troubleshooting steps can be found in [Scanning Troubleshooting](../troubleshooting/scanning.md).

## My scan finds platforms but no games inside them

This is almost always a mount-depth issue. The scanner expects the _parent_ of your `roms/` folder mounted to `/romm/library`, not the `roms/` folder itself. If your files live at `/opt/romm/library/roms/gbc/game.gbc`, mount `/opt/romm/library` to `/romm/library`, then re-scan.

See [Folder Structure](../getting-started/folder-structure.md) and [Scanning Troubleshooting](../troubleshooting/scanning.md) for the full layout and common mount mistakes.

## Why is my metadata wrong or incomplete?

Metadata isn't owned, only pulled from third parties like IGDB and ScreenScraper. If a field is missing or wrong, the fix has to happen upstream on the provider's site. Cross-check against another provider if one is consistently off for your library.

## Why am I getting a "Configuration file not Mounted!" error?

A `config.yml` is read from `/config` at startup. If the mount/file is missing or unreadable, startup bails with this error. See [Configuration File](../reference/configuration-file.md) for the schema and an example you can drop in.

## Can I play PS3 or newer consoles in the browser?

**No.** In-browser emulation handles 4th-gen and earlier systems well. Saturn, PS1, and N64 are hit-or-miss. PSP and newer are mostly unplayable. Browser play is a bonus, as this is a library manager first, and standalone emulators remain the right tool for modern systems. See [Supported Platforms](../platforms/supported-platforms.md) for the current list.

## Why is browser emulation laggy or not loading?

A few common causes:

- **Browser**: use a Chromium-based browser (Chrome, Edge, Brave). Firefox and Safari might run EmulatorJS poorly.
- **HTTPS**: PSP and DOS cores require the site served over `https://`. Accessing by IP won't work, so you need a [Reverse Proxy](../install/reverse-proxy.md) with TLS.
- **Hardware**: EmulatorJS runs entirely in the browser, so CPU-heavy cores need a capable (modern) browser.

Full troubleshooting steps can be found in [In-Browser Play](../troubleshooting/in-browser-play.md).

## Can I share my library with friends?

Add them as users via the invite flow, then either:

- Expose your instance publicly behind a [Reverse Proxy](../install/reverse-proxy.md) with TLS.
- Keep it private and share access over a VPN or Tailscale.

See [Invitations & Registration](../administration/invitations-and-registration.md) and [Mobile & TV → Self-hosting tips](../using/mobile-and-tv.md#self-hosting-tips).

## Are there mobile or handheld companion apps?

Yes, several first-party apps (all in beta or actively developed):

- **[Argosy](../ecosystem/first-party-apps.md#argosy-launcher)**: Android launcher for your library
- **[Grout](../ecosystem/first-party-apps.md#grout)**: companion for Linux-based handhelds (muOS / NextUI and friends)
- **[Playnite Plugin](../ecosystem/first-party-apps.md#playnite-plugin)** for Windows desktop

iOS and other platforms are covered by community-maintained apps listed in the [Community section in the RomM README](https://github.com/rommapp/romm/#community). Full directory: [Ecosystem](../ecosystem/index.md).

## Can guests browse without an account?

Absolutely, just set `KIOSK_MODE=true` in your environment variables and anonymous visitors get read-only access. See [Authentication → Kiosk mode](../administration/authentication.md#kiosk-mode).

## How do I back up?

`mysqldump` the DB + rsync the `/romm/assets` and `/romm/config` volumes nightly. Full procedure + test-restore protocol in [Backup & Restore](../install/backup-and-restore.md).

## Can I use RomM without the internet?

You need internet for:

- First-time scan with metadata providers (they're online APIs)
- Pulling the Docker image on install or upgrade
- OIDC login (if you use a cloud IdP)

After the initial setup, browsing and playing can work offline. In-browser play downloads the emulator bundle on first launch, then caches it.

## Why is scan X slow?

Several possibilities, in rough order of likelihood:

1. Hashing large files on spinning disks.
2. Metadata providers rate-limiting (mostly ScreenScraper).
3. Many files on a network mount with high latency.

[Scanning Troubleshooting → Hash calculations are slow](../troubleshooting/scanning.md#hash-calculations-are-slow).

## When will [feature X] be added?

We don't give ETAs on individual features. Open (or upvote) an issue at [rommapp/romm](https://github.com/rommapp/romm/issues) to make the interest visible.

## What happened to SQLite?

Dropped in 3.0 for stability reasons; use MariaDB, MySQL, or Postgres instead. See [Databases](../install/databases.md).

## I found a bug, or I need help

For bugs, open an issue at [rommapp/romm](https://github.com/rommapp/romm/issues). For questions, ask in `#romm-support` on [Discord](https://discord.gg/romm). Either way, include:

- RomM version
- Deployment (Docker Compose / Unraid / K8s / etc.)
- Your `docker-compose.yml` with credentials and API keys redacted
- Container logs (`docker logs romm`)
- Exact reproduction steps

## Who runs RomM?

A small team of maintainers plus a chunk of active community contributors. Support the project via [Open Collective](https://opencollective.com/romm) if you'd like.

## Where's can I find you?

- **Discord**: [discord.gg/romm](https://discord.gg/romm)
- **GitHub**: [rommapp/romm](https://github.com/rommapp/romm)
- **Website**: [romm.app](https://romm.app/)
- **Demo**: [demo.romm.app](https://demo.romm.app/)
- **Docs**: here ([docs.romm.app](https://docs.romm.app/))

## See also

- [Glossary](../reference/glossary.md) if the vocabulary is new
- [Troubleshooting](../troubleshooting/index.md) if something's broken
- [Release Notes](../releases/index.md) for version-specific questions
