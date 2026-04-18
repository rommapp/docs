---
title: Library
description: Browse your RomM library: dashboard, cards, filters, search, and the platform/game views.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Library

The library is the heart of RomM. This page covers the day-to-day UI: the dashboard, game and platform cards, filters, search, and the detail views.

## Dashboard

Home screen. Several **ribbons** of content:

- **Recently Added**: a carousel of the latest ROMs RomM has indexed.
- **Continue Playing**: games with an active play session. See [Play Sessions](../getting-started/concepts.md#play-session).
- **Platforms**: every platform that has at least one ROM. Cards link into the [platform view](#platform-view).
- **Collections**: your [collections](collections.md), [smart collections](smart-collections.md), and [virtual collections](virtual-collections.md).

Each ribbon can be hidden or shown from **Profile → User Interface**, handy if you prefer a tight dashboard.

## Menu bar

Visible everywhere. Shortcuts to:

- **Search**: global search across every ROM, metadata field, and tag.
- **Platforms**: drawer listing every platform as a link.
- **Collections**: drawer listing every collection type.
- **Scan**: launches a scan. Permission-gated (Admin/Editor).
- **Console Mode**: jumps to the `/console` TV/gamepad UI. See [Console Mode](console-mode.md).
- **Upload**: permission-gated (Admin/Editor). See [Uploads](uploads.md).
- **Profile**: profile drawer + admin panel.

## Grid/list toggle

Every gallery (platform view, collection view, search results) has a grid-vs-list toggle in the top right. Grid is the default: card thumbnails at scale. List is denser: one row per ROM, sortable columns for title, release date, rating, playtime, region.

## Game cards

![game card](https://raw.githubusercontent.com/rommapp/docs/refs/heads/main/docs/resources/usage/gameCard.png)

Hovering over a game card exposes:

- **Play**: launch in [EmulatorJS or Ruffle](in-browser-play.md), if the platform supports in-browser play.
- **Download**: single-file download. See [Downloads](downloads.md) for bulk, QR, and copy-link options.
- **Context menu (…)**: opens the card's action menu.

Card context menu:

![context menu](https://raw.githubusercontent.com/rommapp/docs/refs/heads/main/docs/resources/usage/ContextMenu.png)

- **Match to metadata agent**: manually rematch against a provider (IGDB, ScreenScraper, etc.).
- **Edit**: change title, platform, or other metadata fields (permission-gated).
- **Refresh metadata**: re-query providers and overwrite.
- **Add/remove from Favourites**.
- **Add/remove from Collection**: surfaces your existing collections.

Double-click (or tap) the card to open the [game view](#game-view).

## Filters

Every gallery has a Filters button in the top right. Filter combinations stack, and RomM shows only games matching all active filters.

### Toggle filters

- **Show Unmatched**: games with no provider match.
- **Show Matched**: the inverse.
- **Show Favourites**: your personal favourites.
- **Show Duplicates**: games appearing more than once.
- **Show Playables**: only games with in-browser play support on this platform.
- **Show Missing**: DB entries whose files are gone.
- **Show Verified**: matched via Hasheous.
- **Show RetroAchievements**: games RetroAchievements has achievements for. See [RetroAchievements](retroachievements.md).

### Value filters

Dropdowns that cross-reference metadata on the visible set:

- **Platform**: scope to one platform.
- **Genre / Franchise / Collections / Company / Age Rating / Region / Language**: metadata dimensions.
- **Status**: personal play status (Never Played, Backlogged, Playing, Complete, Hidden).

Filters narrow down *what you're currently viewing*. Search first, filter second, and the filter dropdowns only show values present in the search results.

## Search

Click the search icon in the menu bar. Real-time search against:

- Game title.
- Tags (regions, languages, revisions, arbitrary `[]`/`()` tags).
- Metadata fields (genre, developer, publisher, summary).

Search is platform-aware: type `zelda` and you'll see every matched Zelda across every platform you have.

![search bar](https://raw.githubusercontent.com/rommapp/docs/refs/heads/main/docs/resources/usage/SearchBar.png)

Two icons next to the search bar:

- **View filters**: same filter panel as above.
- **New collection from results**: saves the current search + filter state as a [standard collection](collections.md).

## Platform view

Clicking a platform card takes you to the platform view: every game on that platform, browseable with the same filters and sorts.

![platform drawer](https://raw.githubusercontent.com/rommapp/docs/refs/heads/main/docs/resources/usage/PlatformView.png)

Two side buttons:

- **Platform drawer**: metadata for the platform itself: name, slug, category, generation, IGDB version, active providers, cover-art style setting. Admins see an **Upload** + **Scan** shortcut + a Danger Zone with "Delete Platform" (removes the DB entry, files on disk are not touched, and a rescan re-creates the platform).
- **Firmware**: every firmware file registered against the platform, plus an upload button. See [Firmware Management](../administration/firmware-management.md).

## Collection view

Like the platform view, but scoped to one collection. Same filters and grid/list toggle. The side drawer shows collection metadata (name, owner, visibility, game count) and, for collections you own, Edit and Delete buttons.

Three collection types: see [Collections](collections.md), [Smart Collections](smart-collections.md), [Virtual Collections](virtual-collections.md).

## Game view

Click (or tap) a game. The game view has two halves:

### Left: hero panel

- Cover art (or `vanilla-tilt` 3D hover if enabled in UI settings).
- **Play** button (if playable).
- **Download** button + menu (Copy Link, QR Code, Bulk Download).
- **Upload ROM**: replace / add a new version.
- Context menu: Match, Edit, Match rehash, Delete, etc. (permission-gated).

### Right: tabs

Which tabs appear depends on your metadata providers:

- **Details**: title, description, release date, genres, developer/publisher, regions, rating, matched providers. Filterable metadata surfaces here.
- **Game Data**: save files, save states, screenshots. Per-user. Upload, download, and delete. See [Saves & States](saves-and-states.md).
- **Personal**: your data on this game: status (Never Played / Backlogged / Playing / Complete / Hidden), rating, difficulty, percent complete, notes. Stored per-user.
- **Manual**: PDF viewer if you have a manual for this game.
- **Time to Beat**: [HowLongToBeat](../administration/metadata-providers.md#howlongtobeat) data if enabled.
- **Screenshots**: provider-fetched + user-uploaded screenshots.
- **Achievements**: [RetroAchievements](retroachievements.md) progression if you've linked your RA account.
- **Related Games**: similar titles from IGDB.
- **Additional Content**: DLCs, patches, hacks, mods, translations found inside the multi-file folder.

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| `/` | Focus search. |
| `g h` | Go home. |
| `g s` | Open Search page. |
| `Esc` | Close open drawer or dialog. |

Full shortcut list is on the [Account & Profile](account-and-profile.md) page.

## Console mode alternative

If you're on a TV / gamepad, there's a second UI designed for it: **Console Mode**. Same library, different navigation. See [Console Mode](console-mode.md).
