---
title: Using RomM
description: Browse, play, collect, patch, and share from the UI
---

# Using RomM

## Browse and play

- **[EmulatorJS](in-browser-play/emulatorjs.md)**
    - **[MS-DOS](in-browser-play/ms-dos.md)**
- **[`js-dos`](in-browser-play/js-dos.md)**
- **[PICO-8](in-browser-play/pico-8.md)**
- **[Ruffle](in-browser-play/ruffle.md)**
- **[EasyRPG](in-browser-play/easyrpg.md)**
- **[Emulator Streaming](emulator-streaming.md)**
- **[Downloads](downloads.md)**
- **[Uploads](uploads.md)**
- **[Jukebox](jukebox.md)**

## Organise

- **[Collections](collections.md)**
- **[Smart Collections](smart-collections.md)**
- **[Virtual Collections](virtual-collections.md)**
- **[Physical Games](physical-games.md)**
- **[Recommendations](recommendations.md)**

## Personal data

- **[Saves & States](saves-and-states.md)**
- **[RetroAchievements](retroachievements.md)**
- **[Walkthroughs](walkthroughs.md)**
- **[Account & Profile](account-and-profile.md)**

## Tools

- **[ROM Patcher](rom-patcher.md)**
- **[Netplay](netplay.md)**

## Settings

- **[UI Languages](languages.md)**

## Search

Game search matches a game's title, its file name, and every alternative title RomM knows for it, so a search for a Japanese title finds the game listed under its English name and the other way around. Alternative titles come from IGDB (Hasheous matches included), MobyGames and ScreenScraper, localized and regional names among them. A matched game picks up new alternative titles on its next metadata refresh.

You can also set a game's alternative titles yourself in its manual metadata, for an abbreviation like "ACNH" or a fan translation's name. A hand-set list **replaces** the providers' titles for that game, so include any provider title you still want to match. The API takes it as `alternative_names` in `raw_manual_metadata` on `PUT /api/roms/{id}`, and returns the resolved list as `alternative_names` on the game.

A few more things a search understands:

- **Several searches at once**: separate them with `|`, as in `zelda | metroid`, to match either.
- **Hashes**: a CRC32, MD5, SHA-1 or RetroAchievements hash finds the game whose file has it, including a CHD's uncompressed SHA-1 as DAT files list it.

Until you pick a sort, results are ordered by relevance on every database, with exact title matches (or exact alternative titles) first, then titles that start with your search, then the rest, and multi-word searches favour titles holding the words in order. Once you pick a sort, relevance only breaks ties. In the API, this is an empty `order_by` alongside `search_term` on `GET /api/roms`, and `char_index` comes back empty under relevance order because the results aren't alphabetical.

Platform pickers and the platform list search more than the display name: a platform's slug, its folder name, its abbreviation (such as `SNES` or `PS2`) and its other known names all match. `PlatformSchema` exposes the last two as `abbreviation` and `alternative_names`.
