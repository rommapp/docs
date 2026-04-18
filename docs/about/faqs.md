---
title: FAQs
description: Answers to the questions users most often ask about RomM.
---

# FAQs

## What is RomM?

A self-hosted ROM manager + player. Scan your library, get metadata, browse a clean UI, play in the browser, sync to handhelds, run it on your own hardware.

See [Introduction](../index.md) for the full pitch.

## Is it free?

Yes. [AGPL-3.0](license.md). Core always will be free, and other repos in the umbrella use permissive licenses. No tracking, no upsells.

## How does it compare to [X other manager]?

Not a direct comparison page. Short version: RomM emphasises self-hosted + multi-user + in-browser-play + companion-app ecosystem. If those matter, try RomM. If you just want a local Windows app that scans a folder, tools like LaunchBox may fit better.

## Do I need metadata API keys?

Not strictly. RomM runs without any, but games just won't match to a metadata source, so no covers, descriptions, or ratings.

Recommended: IGDB + ScreenScraper. See [Metadata Providers](../administration/metadata-providers.md) for the full list.

## Is RomM legal?

The software is legal. What you put in it depends on your jurisdiction. We don't ship ROMs or firmware, don't help you find them, and can't give legal advice. General rule: dumping games you own is usually fine, distributing copies is usually not.

## Can I run RomM on [X]?

Probably. Supported deployment paths:

- Docker Compose (Linux, macOS, Windows with WSL).
- Unraid / Synology / TrueNAS SCALE.
- Kubernetes.

See [Install & Deploy](../install/index.md).

Not supported:

- Bare metal without containers (not documented, but may work).
- TrueNAS CORE (FreeBSD, no Docker).
- Windows without WSL (Docker Desktop works, but bare Windows doesn't).

## How much RAM / CPU does it need?

- **Minimum** (small library, 1 user): 512 MB RAM, any modest CPU.
- **Comfortable** (thousands of ROMs, a few users, occasional scans): 2 GB RAM, 2 cores.
- **In-browser play**: browser-side resource-heavy, RomM-server-side negligible.

Heaviest CPU is during scans: hashing + network-bound metadata calls. Plan for spikes.

## How do I update?

```sh
docker compose pull
docker compose up -d
```

Alembic migrations run automatically. Read the release notes before major versions. See [Release Notes & Migration](../releases/index.md).

## Why can't I see a specific platform?

Platform folder name probably doesn't match a known slug. Check [Supported Platforms](../platforms/supported-platforms.md). Fix with either folder rename or a [`system.platforms`](../reference/configuration-file.md#systemplatforms) binding in `config.yml`.

## Why are my ROMs unmatched after a scan?

Most common reasons:

- No metadata providers configured: enable at least one.
- Filename too generic (no tags, unusual naming): add filename tags like `(igdb-1234)` or try another provider.
- Wrong platform detection: see previous FAQ.

Full troubleshooting: [Scanning Troubleshooting](../troubleshooting/scanning.md).

## Can I share my library with friends?

Yes: add them as users via the invite flow, then either share the URL (if accessible to them) or put RomM behind a VPN / Tailscale. See [Invitations & Registration](../administration/invitations-and-registration.md) + [Mobile & TV → Self-hosting tips](../using/mobile-and-tv.md#self-hosting-tips).

## Can guests browse without an account?

Yes: set `KIOSK_MODE=true`. Anonymous visitors get read-only access. See [Authentication → Kiosk mode](../administration/authentication.md#kiosk-mode).

## How do I back up?

`mysqldump` the DB + rsync the `/romm/assets` and `/romm/config` volumes nightly. Full procedure + test-restore protocol in [Backup & Restore](../install/backup-and-restore.md).

## Can I use RomM without the internet?

Mostly. You need internet for:

- First-time scan with metadata providers (they're online APIs).
- Pulling the Docker image on install or upgrade.
- OIDC login (if you use a cloud IdP).

After the initial setup, browsing and playing can work offline. In-browser play downloads the emulator bundle on first launch, then caches it.

## Why is scan X slow?

Several possibilities, in rough order of likelihood:

1. Hashing large files on spinning disks.
2. Metadata providers rate-limiting (mostly ScreenScraper).
3. Many files on a network mount with high latency.

Full troubleshooting: [Scanning Troubleshooting → Hash calculations are slow](../troubleshooting/scanning.md#hash-calculations-are-slow).

## When will [feature X] be added?

We don't give ETAs on individual features. Open (or upvote) an issue at [rommapp/romm](https://github.com/rommapp/romm/issues) to make the interest visible.

For public roadmap-ish information, watch the GitHub Projects board and `#announcements` on Discord.

## What happened to SQLite?

Dropped in 3.0 for stability reasons. Use MariaDB, MySQL, or Postgres instead. See [Databases](../install/databases.md).

## I found a bug.

Open an issue at [rommapp/romm](https://github.com/rommapp/romm/issues) with:

- RomM version.
- Deployment (Docker Compose / Unraid / K8s / etc.).
- Exact repro steps.
- Relevant logs: redact any secrets.

## Who runs RomM?

A small team of maintainers plus a chunk of active community contributors. AGPL-licensed, community-driven. Support the project via [Open Collective](https://opencollective.com/romm) if you'd like.

## Where's Discord / GitHub / the website?

- **Discord**: [discord.gg/romm](https://discord.gg/romm)
- **GitHub**: [rommapp/romm](https://github.com/rommapp/romm)
- **Website**: [romm.app](https://romm.app/)
- **Demo**: [demo.romm.app](https://demo.romm.app/)
- **Docs**: here ([docs.romm.app](https://docs.romm.app/))

## See also

- [Core Concepts](../getting-started/concepts.md): if the vocabulary is new.
- [Troubleshooting](../troubleshooting/index.md): if something's broken.
- [Release Notes](../releases/index.md): for version-specific questions.
