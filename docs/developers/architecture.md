---
title: Architecture
description: High-level walkthrough of the RomM codebase: backend, frontend, nginx, workers.
---

A walkthrough of how RomM is put together, aimed at first-time contributors. The authoritative deep-dives live alongside the code at [`docs/BACKEND_ARCHITECTURE.md`](https://github.com/rommapp/romm/blob/main/docs/BACKEND_ARCHITECTURE.md) and [`docs/FRONTEND_ARCHITECTURE.md`](https://github.com/rommapp/romm/blob/main/docs/FRONTEND_ARCHITECTURE.md) in the main repo.

## Repo layout

```text
rommapp/romm
├── backend/              # Python FastAPI application
│   ├── endpoints/        # Route handlers + Socket.IO under sockets/
│   ├── handler/          # Business logic: database/, metadata/, filesystem/, auth/
│   ├── adapters/services/# External API clients (IGDB, Moby, SS, SGDB, RA, ...)
│   ├── models/           # SQLAlchemy ORM
│   ├── tasks/            # RQ jobs: scheduled/ and manual/
│   ├── alembic/          # 80+ DB migrations
│   └── config/           # Env vars + YAML config manager
├── frontend/             # Vue 3 + Vuetify SPA (main UI + console mode)
│   └── src/
│       ├── views/        # Page-level components
│       ├── components/   # ~168 components, organised by feature
│       ├── console/      # Console Mode SPA (own router, layout, input bus)
│       ├── stores/       # 18 Pinia stores
│       ├── services/     # Axios API modules + Socket.IO + browser cache
│       └── __generated__/# TS types generated from the backend OpenAPI spec
├── docker/               # nginx config, entrypoint, Dockerfiles
└── examples/             # Reference docker-compose.yml and config.yml
```

## Runtime topology

```ascii
┌─────────────────────────────────────────────────────────┐
│ docker container                                        │
│                                                         │
│  ┌───────┐   HTTP   ┌──────────┐  python  ┌──────────┐  │
│  │ nginx │─────────→│ gunicorn │─────────→│ FastAPI  │  │
│  │ :8080 │          │  :5000   │          │ backend  │──┐
│  └───┬───┘          └──────────┘          └──────────┘  │ SQL
│      │   static files (SPA, EmulatorJS, Ruffle)         ↓
│      │   X-Accel-Redirect for downloads          ┌──────────┐
│      │                                           │ MariaDB  │
│      ↓                                           │ (or PG / │
│  /library /assets /resources                     │  MySQL)  │
│  (host bind mounts)                              └──────────┘
│                                                         │
│  ┌──────────┐         ┌──────────────────────┐          │
│  │ RQ       │←───────→│ Valkey               │          │
│  │ workers  │  jobs   │ (embedded or external)│          │
│  └──────────┘         └──────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

- **nginx** serves the SPA bundle, EmulatorJS, Ruffle, and cover art. Proxies API + WebSocket traffic to gunicorn. Streams downloads via `mod_zip` and `X-Accel-Redirect`.
- **gunicorn** runs the FastAPI app under multiple workers (`WEB_SERVER_CONCURRENCY`).
- **FastAPI backend** on Python 3.13+, SQLAlchemy 2.0, `python-socketio`. Talks to the DB, the Valkey cache, and 10+ external metadata providers.
- **RQ workers** pop jobs off three priority queues (`high_prio_queue`, `default_queue`, `low_prio_queue`) backed by Valkey.
- **Valkey** (Redis-compatible) is in-container by default, externalisable. See [Embedded vs External Valkey](../install/redis-or-valkey.md).
- **Database** is always external. MariaDB 10.5+ default. MySQL 8.0+ and PostgreSQL also supported.
- **Filesystem watcher** (optional) enqueues rescans on library changes via `watchfiles`.

## Request lifecycle

The middleware stack runs in front of every route — CORS → CSRF → authentication → Valkey-backed session → context vars (aiohttp + httpx clients) — then FastAPI dispatches to an endpoint that calls into a handler.

A few flows worth knowing:

- **Reads** (`GET /api/roms`) hit `endpoints/roms/__init__.py`, which calls `db_roms_handler` for the SQLAlchemy query and returns a Pydantic schema.
- **Uploads** (`POST /api/roms/upload/*`) are chunked. `init` returns an upload session ID held in Valkey for 24 h. `chunk` pushes up to 64 MB at a time. `complete` assembles, hashes, moves under `/romm/library`, writes the DB row, and emits `rom:created` over Socket.IO.
- **Scans** are enqueued as RQ jobs. The worker walks platform folders, parses filenames, hashes files, queries metadata providers in priority order (IGDB → Moby → SS → LaunchBox → Hasheous → RA → Flashpoint → HLTB → TGDB), downloads artwork, and upserts. Progress streams over Socket.IO. Six modes — `NEW_PLATFORMS`, `QUICK`, `UPDATE`, `UNMATCHED`, `COMPLETE`, `HASHES`.

## Backend

**Layers.** Endpoints validate and serialise. Handlers hold the business logic, split by concern under `handler/database/`, `handler/metadata/`, `handler/filesystem/`, and `handler/auth/`. Models are SQLAlchemy. Adapters wrap external APIs. Roughly 175 HTTP routes and 11 Socket.IO handlers across 24 routers.

**Database.** `roms` is the central entity, linking to `platforms`, `rom_files`, `roms_metadata` (aggregated provider data), `rom_user` (per-user tracking), `rom_notes`, and `sibling_roms` (M:M self-ref for alternate versions). Saves, states, and screenshots FK to both `roms` and `users`. Three collection flavours — manual `collections`, dynamic `smart_collections` (filter-criteria with cached IDs), and read-only `virtual_collections` (a database view, excluded from migrations).

**Auth.** `HybridAuthBackend` walks the methods in order — session cookie, HTTP Basic, OAuth2 Bearer JWT, Client API Token (`rmm_...`, SHA-256 lookup), OIDC, kiosk mode. Token plaintext is never stored. See [API Authentication](api-authentication.md).

**Metadata.** Each provider has a handler under `handler/metadata/` that normalises responses into a common shape. Priority is configurable in `config.yml`. Static fixtures (MAME, ScummVM, PS1/PS2/PSP serial maps, known BIOS hashes) load into Valkey at startup. Hashing is platform-aware — CHD v5, PICO-8, and the RetroAchievements per-platform algorithm all get special handling. Switch and PS3/4/5 skip hashing.

**Configuration.** Env vars (100+, see `env.template`) for infrastructure, plus YAML (`config.yml`) for library/scan/emulator behaviour. `ConfigManager` is a singleton. See [Configuration File](../reference/configuration-file.md).

## Frontend

Vue 3 + Composition API + TypeScript, built with Vite. UI is Vuetify 3 plus Tailwind CSS 4. State lives in 18 Pinia stores (auth, ROMs, platforms, collections, gallery filters, scan progress, etc.). Vue Router covers 36 named routes across three layouts — Auth (public), Main (authenticated), and Console (gamepad/TV). Translations via vue-i18n in 17 locales. Mitt is used as a loose event bus to trigger dialogs from anywhere.

TypeScript types in `src/__generated__/` are generated from the backend OpenAPI spec via `npm run generate`, giving type-safe end-to-end communication.

The Axios instance carries a 2-minute timeout, injects the CSRF token from the `romm_csrftoken` cookie, and on 403 clears the session and redirects to `/login`. UI preferences persist to localStorage and sync to `user.ui_settings` on the backend.

**Console Mode** is a second SPA bundle for TV and gamepad. Stack-based input bus, grid-based spatial navigation, gamepad polling in `requestAnimationFrame`, and SFX synthesised via the Web Audio API.

## Background jobs

RQ workers run scheduled jobs (rescans, Switch TitleDB refresh, LaunchBox refresh, image-to-WebP conversion, RA progress sync, netplay cleanup) and manual tasks (`cleanup_missing_roms`, `cleanup_orphaned_resources`, `sync_folder_scan`). Each scheduled task is gated by an `ENABLE_SCHEDULED_*` env var.

Jobs persist to Valkey, so restarts don't lose in-flight work — but only if `appendonly` is on.

## Real-time

Two Socket.IO servers, both Valkey-backed for horizontal scaling — `/ws` for scan progress and notifications, `/netplay` for netplay rooms. See [WebSockets](websockets.md).

## Filesystem layout

```text
{ROMM_BASE_PATH}/                # Default: /romm
├── library/{platform_slug}/     # ROMs (roms/) and BIOS (bios/)
├── resources/roms/{rom_id}/     # Cached cover art + screenshots
├── assets/users/{user_id}/      # User saves, states, screenshots
└── config/config.yml            # YAML configuration
```

## Observability

Sentry (opt-in via `SENTRY_DSN`) captures unhandled exceptions. OpenTelemetry (opt-in) ships traces, metrics, and logs over OTLP. `GET /api/heartbeat` returns an aggregated health snapshot, safe to scrape from uptime monitors. See [Observability](../administration/observability.md).

## Contributing

See [Contributing](contributing.md) for process and style. For non-trivial backend changes, read the relevant handler in `backend/handler/` first.

## See also

- [Development Setup](development-setup.md): get a local env running
- [API Reference](api-reference.md): what the backend exposes
- [API Authentication](api-authentication.md): auth modes in detail
- [WebSockets](websockets.md): Socket.IO endpoints
- [Configuration File](../reference/configuration-file.md): `config.yml` schema
- [Embedded vs External Valkey](../install/redis-or-valkey.md): cache + queue store
