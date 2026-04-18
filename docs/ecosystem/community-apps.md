---
title: Community Apps
description: Third-party companion apps for RomM — maintained by the community, not the RomM team.
---

# Community Apps

Apps listed here are **community-maintained**. The RomM team doesn't build or officially support them — the authors do. Support is via the individual app's issue tracker and the RomM Discord.

First-party alternatives (built by the RomM team):

- [Argosy Launcher](argosy.md) (Android).
- [Grout](grout.md) (Linux handhelds).
- [Playnite Plugin](playnite-plugin.md) (Windows).
- [muOS App](muos-app.md) (muOS handhelds).

## Mobile

### romm-ios-app

Native iOS client for RomM.

- **Author:** [@ilyas-hallak](https://github.com/ilyas-hallak)
- **Platform:** iOS
- **Status:** Active

### romm-mobile

Android + iOS client.

- **Author:** [@mattsays](https://github.com/mattsays)
- **Platform:** Android (iOS in progress)
- **Status:** Active

## Desktop

### RommBrowser

Electron-based desktop browser for RomM.

- **Author:** [@smurflabs](https://github.com/smurflabs)
- **Platform:** Windows, macOS, Linux
- **Status:** Active

### RomMate

Desktop app for browsing.

- **Author:** [@brenoprata10](https://github.com/brenoprata10)
- **Platform:** Windows, macOS, Linux
- **Status:** Active

### romm-client

Another desktop client.

- **Author:** [@chaun14](https://github.com/chaun14)
- **Platform:** Desktop
- **Status:** Active

### RetroArch Sync

Sync your RetroArch library with RomM.

- **Author:** [@Covin90](https://github.com/Covin90)
- **Platform:** Anywhere RetroArch runs
- **Status:** Active

## Handhelds

### DeckRommSync

SteamOS downloader/syncer for Steam Deck.

- **Author:** [@PeriBluGaming](https://github.com/PeriBluGaming)
- **Platform:** Steam Deck (SteamOS)
- **Status:** Active

### SwitchRomM

Homebrew NRO app for Nintendo Switch — pull ROMs from RomM over Wi-Fi.

- **Author:** [@Shalasere](https://github.com/Shalasere)
- **Platform:** Nintendo Switch (homebrew)
- **Status:** Active

## Services

### romm-comm

Discord bot for interacting with RomM from a Discord server — query library, post stats, request games.

- **Author:** [@idio-sync](https://github.com/idio-sync)
- **Platform:** Discord bot
- **Status:** Active

### GGRequestz

Game discovery and request tracker that integrates with RomM.

- **Author:** [@XTREEMMAK](https://github.com/XTREEMMAK)
- **Platform:** Web service
- **Status:** Active

### Syncthing Sync

Push a Syncthing-managed library to RomM automatically.

- **Author:** [@amn-96](https://github.com/amn-96)
- **Platform:** Wherever Syncthing runs
- **Status:** Active

## "Community-maintained" — what it means

- **The RomM team doesn't build these.** We won't fix bugs, ship features, or respond to support tickets for community apps.
- **Support through the app author.** Each project has its own issue tracker — use it.
- **Install at your own risk.** We don't code-review community apps or vouch for their security posture.
- **Token safety.** These apps use [Client API Tokens](client-api-tokens.md) the same way first-party apps do. Scope tokens narrowly and revoke if an app misbehaves.

## Submitting a new app

Built something? Open a PR on [rommapp/docs](https://github.com/rommapp/docs) adding your project to this list with:

- Name, short description.
- Author GitHub handle.
- Platform(s).
- Repo link.
- Status (Active / Maintenance-mode / Abandoned).

We'll merge if the project's real, has a working repo, and isn't obviously broken.

## Reporting an abandoned app

If an app here hasn't been updated in >12 months and the maintainer isn't responsive, let us know — either a PR marking it as Abandoned, or a Discord message in `#community-projects`. We flag abandoned projects so users know not to rely on them.
