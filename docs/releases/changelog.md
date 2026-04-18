---
title: Changelog
description: Summary of notable RomM releases; authoritative per-release notes live on GitHub.
---

# Changelog

This page summarises major RomM releases. **The authoritative per-release changelog lives on [GitHub Releases](https://github.com/rommapp/romm/releases)**; every tag there has full commit lists, breaking changes flagged, and upgrade notes.

For migration-grade detail on a major version, go straight to that version's guide:

- **[Upgrading to 5.0](upgrading-to-5.0.md)**
- **[Upgrading to 3.0](upgrading-to-3.0.md)**

## 5.0

[What's New in 5.0](../getting-started/what-is-new-in-5.md) · [Upgrading to 5.0](upgrading-to-5.0.md) · [GitHub Release](https://github.com/rommapp/romm/releases/tag/5.0.0)

The biggest release since the project started. Highlights:

- **Console Mode:** a gamepad-first `/console` UI for TVs.
- **Smart & Virtual Collections:** rule-based and auto-generated collections.
- **ROM Patcher:** apply IPS/UPS/BPS/PPF and more in-browser.
- **Netplay:** EmulatorJS multiplayer with ICE servers.
- **Device sync protocol** + Client API Tokens with device pairing.
- **OIDC role mapping** via claims (`OIDC_CLAIM_ROLES`).
- **Thirteen metadata providers:** added TheGamesDB, Libretro, gamelist.xml importer.
- **PWA install** support.
- **19 locales**.
- **OpenTelemetry** export via `OTEL_ENABLED`.
- **Slim + Full image variants**.

## 4.x

Highlights rolled up:

- **4.8:** stability and per-platform stats opt-in.
- **4.x:** iterative improvements on the 3.x → 4.x baseline: expanded metadata sources, frontend polish, first-class companion-app support.

The 4.x docs live at [docs.romm.app/4.8/](https://docs.romm.app/4.8/) as a frozen snapshot. See [Release Notes & Migration → Docs versions](index.md#docs-versions).

## 3.0

[Upgrading to 3.0](upgrading-to-3.0.md) · [GitHub Release](https://github.com/rommapp/romm/releases/tag/3.0.0)

Watershed release that made RomM a real multi-user platform:

- **Required authentication:** no more unauthenticated mode.
- **SQLite support dropped:** MariaDB became the default.
- **Redis built-in:** the experimental Redis add-on was absorbed.
- **Saves, states, and screenshots:** first-class user asset management.
- **Config moved to a folder mount** (`/romm/config`).

## Older

2.x and earlier aren't supported and aren't covered by migration guides. Upgrade to 3.x using the 3.0 guide, then to 5.x using the 5.0 guide.

## Want release pings?

- Watch the [rommapp/romm](https://github.com/rommapp/romm) repo on GitHub: "Custom → Releases" for release-only notifications.
- Join the [Discord](https://discord.gg/romm) and look for `#announcements`.
