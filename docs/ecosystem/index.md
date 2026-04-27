---
title: Integrations & Ecosystem
description: Companion apps, feeds, and protocol references for building on top of RomM.
---

# Integrations & Ecosystem

RomM has a sizeable ecosystem of companion apps and integration patterns. This hub indexes everything: first-party and community.

## First-party apps

Maintained by the RomM team.

- **[Argosy Launcher](first-party-apps.md#argosy-launcher)**: Android launcher that browses and launches your RomM library on mobile
- **[Grout](first-party-apps.md#grout)**: Linux handheld companion for muOS / NextUI devices
- **[Playnite Plugin](first-party-apps.md#playnite-plugin)**: Windows desktop, imports your RomM library into [Playnite](https://playnite.link)

## Feeds (for third-party apps)

RomM exposes several URL feed endpoints for external homebrew / custom firmware apps that already know how to consume them.

- **[Tinfoil](feed-clients.md#tinfoil)**: Nintendo Switch homebrew for installing `.nsp` / `.xci` from a URL
- **[pkgj](feed-clients.md#pkgj)**: PS Vita and PSP homebrew installer
- **[fpkgi](feed-clients.md#fpkgi)**: PS4 / PS5 installer
- **[Kekatsu](feed-clients.md#kekatsu)**: Nintendo DS multiboot loader
- **[WebRcade](feed-clients.md#webrcade)**: browser-based retro console frontend

See the [full feeds reference](../reference/feeds.md) for URL formats, auth requirements, and filtering.

## Community apps

Maintained by individuals in the community, not the RomM team, so support quality varies.

See **[Community Apps](community-apps.md)** for the full list with status flags (active / maintenance-mode / abandoned) and links.

Highlights:

- **romm-ios-app** (iOS native)
- **romm-mobile** (Android + iOS)
- **RommBrowser** (Electron desktop)
- **RomMate** (desktop)
- **romm-client** (desktop)
- **DeckRommSync** (Steam Deck)
- **SwitchRomM** (Nintendo Switch homebrew NRO)
- **RetroArch Sync**
- **romm-comm** (Discord bot)
- **GGRequestz** (game request tracker)
- **Syncthing Sync**

## Build your own

For developers building something new on top of RomM:

- **[Client API Tokens](client-api-tokens.md)**: how to authenticate your app, how the device-pairing flow works
- **[Device Sync Protocol](device-sync-protocol.md)**: wire-level reference for save/state/play-session sync
- **[SSH Sync](ssh-sync.md)**: server-side SSH config for push/pull sync to handhelds
- **[API Reference](../developers/api-reference.md)**: every REST endpoint
- **[WebSockets](../developers/websockets.md)**: live-update channels and Netplay coordination
- **[Consuming OpenAPI](../developers/openapi.md)**: codegen patterns

## External tooling

Not a RomM companion but useful alongside:

- **[Igir Collection Manager](igir.md)**: ROM sorting/verifying tool that cleans up library layout before importing into RomM

## Contributing a companion app

Built something RomM-adjacent? Open a PR on [rommapp/docs](https://github.com/rommapp/docs) adding it to [Community Apps](community-apps.md), or drop a link in the [Discord](https://discord.gg/romm) `#community-projects` channel.

We list active, maintained projects, with no gate on code quality but we do flag abandoned projects so users know what's current.
