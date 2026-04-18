---
title: Credits
description: The humans, projects, and services that make RomM possible.
---

# Credits

RomM exists because a lot of people contributed code, designs, translations, ideas, and, most importantly, running bug reports back to the project. Thanks to every one of them.

## Core maintainers

The small team that reviews PRs, cuts releases, and keeps the project moving. Check [rommapp/romm](https://github.com/rommapp/romm/graphs/contributors) for the current active list. Credits here would drift.

## Contributors

[Every contributor](https://github.com/rommapp/romm/graphs/contributors) to [rommapp/romm](https://github.com/rommapp/romm), plus contributors to the surrounding repos:

- [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher/graphs/contributors)
- [rommapp/grout](https://github.com/rommapp/grout/graphs/contributors)
- [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin/graphs/contributors)
- [rommapp/muos-app](https://github.com/rommapp/muos-app/graphs/contributors)
- [rommapp/docs](https://github.com/rommapp/docs/graphs/contributors)

## Translators

RomM's 19 locales exist because individual community members took the time to translate the UI. See each locale folder's commit history at [rommapp/romm/tree/master/frontend/src/locales](https://github.com/rommapp/romm/tree/master/frontend/src/locales) for per-locale credit.

## Community apps

Built by the community, not the RomM team. Full list in [Community Apps](../ecosystem/community-apps.md).

## Upstream projects

RomM stands on an enormous amount of open-source work. In rough order of "how visible they are to users":

### In-browser emulation

- [EmulatorJS](https://emulatorjs.org/): the retro emulator that powers most of our in-browser play.
- [Ruffle](https://ruffle.rs/): the Flash / Shockwave emulator.
- [dosbox-pure](https://github.com/schellingb/dosbox-pure): DOS emulation core via EmulatorJS.

### Metadata sources

- [IGDB](https://www.igdb.com/): the Internet Game Database.
- [ScreenScraper](https://screenscraper.fr/): French community metadata.
- [MobyGames](https://www.mobygames.com/): game database.
- [RetroAchievements](https://retroachievements.org/): achievements and hash matching.
- [SteamGridDB](https://www.steamgriddb.com/): cover art.
- [Hasheous](https://hasheous.org/): hash-based matching.
- [PlayMatch](https://github.com/RetroRealm/playmatch): community hash service.
- [LaunchBox Games Database](https://gamesdb.launchbox-app.com/): local metadata DB.
- [TheGamesDB](https://thegamesdb.net/): free community DB.
- [Flashpoint Archive](https://flashpointproject.github.io/flashpoint-database/): Flash game preservation.
- [HowLongToBeat](https://howlongtobeat.com/): completion times.
- [Libretro](https://www.libretro.com/): core metadata.

### Backend stack

- [FastAPI](https://fastapi.tiangolo.com/) + [Starlette](https://www.starlette.io/): the web framework.
- [SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/): ORM and migrations.
- [RQ](https://python-rq.org/): background job queue.
- [MariaDB](https://mariadb.org/) / [PostgreSQL](https://www.postgresql.org/) / [MySQL](https://www.mysql.com/): database backends.
- [Redis](https://redis.io/) / [Valkey](https://valkey.io/): cache and queue.
- [nginx](https://nginx.org/) with [`mod_zip`](https://github.com/evanmiller/mod_zip): reverse proxy + streaming zip downloads.
- [uv](https://docs.astral.sh/uv/): Python package manager.

### Frontend stack

- [Vue 3](https://vuejs.org/): frontend framework.
- [Vuetify](https://vuetifyjs.com/): component library.
- [Pinia](https://pinia.vuejs.org/): state management.
- [Vite](https://vitejs.dev/): build tool.
- [Socket.IO](https://socket.io/): real-time communication.
- [vue-i18n](https://vue-i18n.intlify.dev/): localisation.
- [rom-patcher-js](https://www.marcrobledo.com/RomPatcher.js/): the ROM patcher library.
- [vite-plugin-pwa](https://vite-pwa-org.netlify.app/): PWA support.

### Docs stack

- [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/): what you're reading.
- [mike](https://github.com/jimporter/mike): docs versioning.
- [asciinema](https://asciinema.org/): terminal recordings.

## Community

- [#selfh.st](https://selfh.st/): early visibility for the project.
- [Hacker News](https://news.ycombinator.com/): the launch-day bump.
- [Aikido Security](https://www.aikido.dev/): security audit.
- Everyone who submitted a bug report, pinged Discord, or pushed a typo fix.

## Financial supporters

Donors via [Open Collective](https://opencollective.com/romm) make continued development possible. The project wouldn't exist without you. Thanks.

## Missing?

Open a PR against this page. Credit is cheap, and we'd rather err on the side of naming everyone than leaving someone out.

## See also

- [License](license.md): the legal bit.
- [Contributing](../developers/contributing.md): if you want to be on this list.
