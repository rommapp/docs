---
title: Integrations & Ecosystem
description: Companion apps, feeds, and protocol references
---

# Integrations & Ecosystem

RomM has a sizeable ecosystem of companion apps and integration patterns.

## First-party apps

Maintained by the team:

- **[Argosy Launcher](first-party-apps.md#argosy-launcher)**: Android launcher that browses and launches your library on mobile
- **[Grout](first-party-apps.md#grout)**: Linux handheld companion for muOS / NextUI devices
- **[Playnite Plugin](first-party-apps.md#playnite-plugin)**: Windows desktop, imports your library into [Playnite](https://playnite.link)

## Feeds (for third-party apps)

RomM exposes several URL feed endpoints for external homebrew / custom firmware apps that already know how to consume them.

- **[Tinfoil](feed-clients.md#tinfoil)**: Nintendo Switch homebrew for installing `.nsp` / `.xci` from a URL
- **[pkgj](feed-clients.md#pkgj)**: PS Vita and PSP homebrew installer
- **[pkgi](feed-clients.md#pkgi)**: PS3 / PS Vita / PSP installer (older CSV format)
- **[fpkgi](feed-clients.md#fpkgi)**: PS4 / PS5 installer
- **[Kekatsu](feed-clients.md#kekatsu)**: Nintendo DS multiboot loader

## Community apps

Maintained by individuals in the community, not the team, so support quality varies.

See the **[Community section in the README](https://github.com/rommapp/romm/#community)** for the full list with status flags (active / maintenance-mode / abandoned) and links.

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

Built something adjacent? Open a PR on [rommapp/romm](https://github.com/rommapp/romm) adding it to the [Community section in the README](https://github.com/rommapp/romm/#community), or drop a link in the [Discord](https://discord.gg/romm) `#community-projects` channel.

We list active, maintained projects, with no gate on code quality, but we do flag abandoned projects so users know what's current.
