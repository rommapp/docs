---
title: Glossary
description: The vocabulary every page assumes you know
---

# Glossary

Every term the docs, UI, and API use consistently, with foundational concepts getting a paragraph, lookups a single sentence, and almost every entry linking out to a dedicated page for full detail.

---

**Admin**: highest user role. Full scope set, including user management and task execution (see [Users & Roles](../administration/users-and-roles.md)).

**API token**: see Client API Token.

**Asset**: user-uploaded content attached to a ROM, such as save files, emulator states, and screenshots. Assets live under `/romm/assets` (separate from the library) and are owned per-user. Saves and states can sync to registered devices, and are not the same as a Resource (see [Saves & States](../using/saves-and-states.md)).

**Autologin**: OIDC feature that bypasses the login page and redirects straight to the IdP. Set via `OIDC_AUTOLOGIN=true`.

**Basic auth**: HTTP auth with username+password in a header. Supported for API calls.

**BIOS**: see Firmware.

**Client API Token**: long-lived bearer token scoped to a user. Used by companion apps (Argosy, Grout, Playnite, custom scripts) to authenticate. Each user gets up to 25 active tokens, and tokens can be paired to devices via a short code (see [Client API Tokens](../developers/client-api-tokens.md)).

**Collection**: a named grouping of ROMs (see [Collections](../using/collections.md)).

**Device**: a registered endpoint that syncs with RomM, such as a handheld running Grout, an Android phone running Argosy, or a SteamDeck running DeckRommSync. Devices pull saves and states, and some push them back after a session (see [Device Sync Protocol](../developers/device-sync-protocol.md)).

**EmulatorJS**: the bundled in-browser retro emulator. Handles NES, SNES, N64, PSX, Saturn, and 20+ more cores (see [In-Browser Play → EmulatorJS](../using/in-browser-play/emulatorjs.md)).

**Facet**: one axis a [recommendation](../using/recommendations.md) is explained by, such as a shared franchise, genre, theme or developer. A facet counts for as much as it is rare in your own library.

**Feed**: a URL endpoint that exposes a filtered library view in a third-party tool's expected format (see [Feed Clients](../ecosystem/feed-clients.md)).

**Firmware**: BIOS or system firmware required for certain emulators (PS1, GBA, Saturn, etc.). Lives wherever the [`filesystem.structure.firmware`](configuration-file.md#filesystemstructure) template points, `bios/{platform}` by default. Uploaded via the UI and managed by admins and users with the `firmware.write` scope (see [Firmware Management](../administration/firmware-management.md)).

**Full image**: the default container variant, bundling all four browser runtimes (EmulatorJS, Ruffle, `js-dos`, FAKE-08). `rommapp/romm:X.Y.Z` (see [Image Variants](../install/image-variants.md)).

**Game Data tab**: the ROM detail page tab for saves, states, and screenshots. User-specific.

**gamelist.xml**: ES-DE/Batocera-compatible metadata format. Importable as a metadata source and exportable.

**Jukebox**: the library-wide soundtrack player, reading the audio files in each game's `soundtrack/` folder (see [Jukebox](../using/jukebox.md)).

**Invite link**: single-use URL that lets a new user register with a pre-assigned role (see [Invitations & Registration](../administration/invitations-and-registration.md)).

**Kekatsu**: Nintendo DS multiboot loader that reads RomM's feed (see [Kekatsu](../ecosystem/feed-clients.md#kekatsu)).

**Kiosk mode**: server-side setting (`KIOSK_MODE=true`) that turns every read endpoint into unauthenticated access. Anonymous visitors can browse but nobody can write, which fits public demos and wall displays (see [Authentication → Kiosk mode](../administration/authentication.md#kiosk-mode)).

**Library**: your ROM files on disk. Mounted at `/romm/library` inside the container, and laid out according to your [structure templates](../getting-started/folder-structure.md#custom-library-structure). The catalogue is built from what's found there (see [Folder Structure](../getting-started/folder-structure.md)).

**Metadata provider**: external source of game data, queried during a scan, with results merged. Configured via env vars + priority in `config.yml` (see [Metadata Providers](../getting-started/metadata-providers.md)).

**Memory card**: on PS2 and GameCube, the emulator's whole card kept in your RomM library rather than on the streaming container, with versions and sharing (see [Emulator Streaming → Memory cards](../using/emulator-streaming.md#memory-cards)).

**Netplay**: EmulatorJS's multiplayer mode. Two or more players share a session across the internet. Open rooms are tracked and brokered via WebSocket. Needs STUN/TURN (ICE servers) configured in `config.yml` for reliable NAT traversal (see [Netplay](../using/netplay.md)).

**OIDC**: OpenID Connect. Supported SSO protocol for external auth (see [OIDC Setup](../administration/oidc/index.md)).

**OpenTelemetry (OTEL)**: opt-in traces/metrics/logs export. `OTEL_ENABLED=true` (see [Observability](../administration/observability.md)).

**Permission group**: a named template of capabilities (a grant matrix over entity types × `read`/`write`/`delete`) assigned to a User. One group is the server-wide default for new users. Admins bypass groups entirely (see [Users & Roles](../administration/users-and-roles.md#permission-groups)).

**Personal tab**: the ROM detail page tab for per-user data (rating, status, notes, playtime).

**Platform**: a gaming system: SNES, PlayStation, Game Boy Advance, DOS, etc. ~400 platforms ship supported. Each has a **slug** (`snes`, `psx`, `gba`) that doubles as the folder name expected in your library, alongside the [folder name aliases](../platforms/supported-platforms.md#folder-name-aliases) other frontends use. Override the folder-name → slug mapping via `config.yml` (see [Supported Platforms](../platforms/supported-platforms.md)).

**Physical game**: a library entry for a copy you own on cartridge or disc, with no file on disk. Added by name or by barcode, and excluded from anything that needs a real file (see [Physical Games](../using/physical-games.md)).

**Play session**: a timestamped record of someone playing a ROM (start, end, duration, device). Used by the stats, the Continue Playing ribbon, and per-ROM playtime totals. Ingested automatically when playing in-browser, and companion apps push them via API.

**PWA**: Progressive Web App. Install RomM to your phone or desktop home screen via your browser's add-to-home-screen flow. Requires HTTPS.

**Resource**: provider-fetched metadata image (cover art, screenshot, manual) stored under `/romm/resources`. **Machine-managed** and rebuildable from a rescan. Not the same as an Asset (`/romm/assets`), which is user-owned and not recoverable from the library.

**ROM**: a single game entry. One filesystem file, one folder of files (multi-disc, patched, with DLC), or a manual DB entry. Each ROM belongs to exactly one platform. ROMs get metadata (cover, description, ratings, related games), user data (per-user rating, notes, playtime), and optional assets (saves, states, screenshots, firmware).

**Role**: an account's top-level type. Two roles: User (access governed by a permission group) and Admin (full access, bypasses groups). See [Users & Roles](../administration/users-and-roles.md).

**Ruffle**: the bundled in-browser Flash/Shockwave emulator (see [In-Browser Play → Ruffle](../using/in-browser-play/ruffle.md)).

**Scan**: the process of walking the library, hashing files, calling metadata providers, and updating the DB. Scans run in six **modes** (New Platforms, Quick, Unmatched, Update, Hashes, Complete) and can be triggered manually, on a cron, or by the filesystem watcher (see [Scanning & Watcher](../administration/scanning-and-watcher.md)).

**Session (streaming)**: one claim on a streaming container. A container drives one display, so it holds one session at a time, bound to the user who claimed it (see [Emulator Streaming](../using/emulator-streaming.md#how-a-session-works)).

**Scope**: a coarse OAuth permission derived from a user's effective [permission-group](../administration/users-and-roles.md#permission-groups) grants. Client API Tokens and OIDC sessions carry a subset of the user's scopes (see [Users & Roles → API tokens](../administration/users-and-roles.md#api-tokens-advanced)).

**Setup Wizard**: first-run flow that creates the admin user. Shown before any user exists.

**Smart Collection**: rule-based auto-populating collection (see [Smart Collections](../using/smart-collections.md)).

**socket.io**: the WebSocket protocol. Two endpoints: `/ws` and `/netplay` (see [WebSockets](../developers/websockets.md)).

**Task**: a unit of background work (scan, metadata sync, cleanup, device sync). Runs through RQ. Can be scheduled (cron), watcher-triggered, or manual (see [Scheduled Tasks](../administration/scheduled-tasks.md)).

**Title id**: the platform-native identifier read out of a ROM's own binary during a scan, on the platforms that have one. Identifies a game where RomM doesn't hash, and says where the game writes its saves (see [Scanning & Watcher](../administration/scanning-and-watcher.md#title-ids-read-from-the-binary)).

**Tinfoil**: Nintendo Switch homebrew that installs from RomM's feed (see [Tinfoil](../ecosystem/feed-clients.md#tinfoil)).

**User**: an account. Its role is either User (access from a permission group plus per-user overrides) or Admin (full access). Can be created by the Setup Wizard, an admin, an invite link, or OIDC auto-provisioning (see [Users & Roles](../administration/users-and-roles.md)).

**Valkey**: open-source Redis fork, drop-in compatible (see [Redis or Valkey](../install/redis-or-valkey.md)).

**Virtual Collection**: auto-generated collection by genre/developer/year/tag. Read-only (see [Virtual Collections](../using/virtual-collections.md)).

**Walkthrough**: a guide document attached to a game, stored in its `walkthrough/` folder beside its manual, uploaded or imported from a GameFAQs URL, with per-user reading progress (see [Walkthroughs](../using/walkthroughs.md)).

**Watcher**: filesystem watcher that triggers scans on file events. `ENABLE_RESCAN_ON_FILESYSTEM_CHANGE=true` (see [Scanning & Watcher](../administration/scanning-and-watcher.md#filesystem-watcher)).

**webstation**: the single container every streamed emulator runs in, serving as many platforms as you point at it (see [Emulator Streaming](../using/emulator-streaming.md)).

---

Missing a term? Open a PR against this page.
