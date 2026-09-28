---
title: Integrations & Ecosystem
description: Companion apps, feeds, and protocol references
---

# Integrations & Ecosystem

RomM works with first-party and community companion apps, URL feeds for third-party clients, and protocol references for building your own.

## First-party apps

Maintained by the team:

- **[Argosy Launcher](first-party-apps.md#argosy-launcher)**: Android launcher that browses and launches your library on mobile
- **[Grout](first-party-apps.md#grout)**: Linux handheld companion for muOS/NextUI devices
- **[Playnite Plugin](first-party-apps.md#playnite-plugin)**: Windows desktop, imports your library into [Playnite](https://playnite.link)

To see which apps sync saves, track playtime or download games for each system, see the [App Feature Comparison](app-comparison.md).

## Feeds (for third-party apps)

RomM exposes several URL feed endpoints for external homebrew/custom firmware apps that already know how to consume them.

- **[Tinfoil](feed-clients.md#tinfoil)**: Nintendo Switch homebrew for installing `.nsp`/`.xci` from a URL
- **[pkgj](feed-clients.md#pkgj)**: PS Vita and PSP homebrew installer
- **[pkgi](feed-clients.md#pkgi)**: PS3/PS Vita/PSP installer (older CSV format)
- **[fpkgi](feed-clients.md#fpkgi)**: PS4/PS5 installer
- **[Kekatsu](feed-clients.md#kekatsu)**: Nintendo DS multiboot loader

## Community apps

Individuals in the community, not the team, maintain these apps, so support quality varies.

See the [Community section in the README](https://github.com/rommapp/romm/#community) for the full list with status flags (active/maintenance-mode/abandoned) and links.

As of September 2026:

- **romm-ios-app** (iOS native)
- **RetroArch Sync** (Linux desktop, syncs RetroArch saves and states)
- **RomMate** (desktop)
- **romm-client** (desktop)
- **Freegosy** (desktop game manager)
- **Tender**, formerly DeckyRommSync (Steam Deck)
- **SwitchRomM** (Nintendo Switch homebrew NRO)
- **romm-comm** (Discord bot)
- **GGRequestz** (game request tracker)
- **Syncthing sync** (pushes saves and states from a Syncthing folder)

The [App Feature Comparison](app-comparison.md) covers what each of these supports.

## Build your own

For developers building something new on top of RomM:

- **[Client API Tokens](../developers/client-api-tokens.md)**: how to authenticate your app, how the device-pairing flow works
- **[Device Sync Protocol](../developers/device-sync-protocol.md)**: wire-level reference for save/state/play-session sync
- **[SSH Sync](../developers/ssh-sync.md)**: server-side SSH config for push/pull sync to handhelds
- **[API Reference](../developers/api-reference.md)**: every REST endpoint
- **[WebSockets](../developers/websockets.md)**: live-update channels and Netplay coordination
- **[Consuming OpenAPI](../developers/openapi.md)**: codegen patterns

## External tooling

Not a companion app but useful:

- **[Igir Collection Manager](igir.md)**: ROM sorting/verifying tool that cleans up library layout

## Contributing a companion app

If you've built something related, open a PR on [rommapp/romm](https://github.com/rommapp/romm) adding it to the [Community section in the README](https://github.com/rommapp/romm/#community), or drop a link in the [Discord](https://discord.gg/romm) `#community-projects` channel.

We list active, maintained projects without reviewing code quality, and we flag abandoned projects so users know what's current.
