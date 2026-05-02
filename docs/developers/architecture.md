---
title: Architecture
description: High-level walkthrough of the codebase
---

# Architecture

What you need to know to find your way around `rommapp/romm` before you start changing things. The exhaustive deep-dives live alongside the code at [`docs/BACKEND_ARCHITECTURE.md`](https://github.com/rommapp/romm/blob/main/docs/BACKEND_ARCHITECTURE.md) and [`docs/FRONTEND_ARCHITECTURE.md`](https://github.com/rommapp/romm/blob/main/docs/FRONTEND_ARCHITECTURE.md). This page is the orientation pass.

## Repo layout

```text
rommapp/romm
├── backend/              # Python FastAPI application
│   ├── endpoints/        # Route handlers + socket.io under sockets/
│   ├── handler/          # Business logic: database/, metadata/, filesystem/, auth/
│   ├── adapters/services/# External API clients (IGDB, Moby, SS, SGDB, RA, ...)
│   ├── models/           # SQLAlchemy ORM
│   ├── tasks/            # RQ jobs: scheduled/ and manual/
│   ├── alembic/          # 80+ DB migrations
│   └── config/           # Env vars + YAML config.json manager
├── frontend/             # Vue 3 + Vuetify SPA (main UI + Console Mode)
│   └── src/
│       ├── views/        # Page-level components
│       ├── components/   # ~168 components, organised by feature
│       ├── console/      # Console Mode SPA (own router, layout, input bus)
│       ├── stores/       # 18 Pinia stores
│       ├── services/     # Axios API modules + socket.io + browser cache
│       └── __generated__/# TS types generated from the backend OpenAPI spec
├── docker/               # nginx config, entrypoint, Dockerfiles
└── examples/             # Reference docker-compose.yml and config.yml
```

## Runtime topology

A running RomM container hosts several cooperating processes:

```ascii
┌─────────────────────────────────────────────────────────┐
│ docker container                                        │
│                                                         │
│  ┌───────┐   HTTP   ┌──────────┐  python  ┌──────────┐  │
│  │ nginx │─────────→│ gunicorn │─────────→│ FastAPI  │  │
│  │ :8080 │          │  :5000   │          │ backend  │──┐
│  └───┬───┘          └──────────┘          └──────────┘  │ SQL
│      │   static files (SPA, EmulatorJS, Ruffle)         ↓
│      │                                           ┌──────────┐
│      │                                           │ MariaDB  │
│      ↓                                           │ (or PG/│
│  /library /assets /resources                     │  MySQL)  │
│  (host bind mounts)                              └──────────┘
│                                                         │
│  ┌──────────┐         ┌──────────────────────┐          │
│  │ RQ       │←───────→│ Valkey               │          │
│  │ workers  │  jobs   │ (embedded or external)│          │
│  └──────────┘         └──────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

## Request lifecycle

Every request runs the middleware stack in order, CORS → CSRF → authentication → Valkey-backed session → context vars (aiohttp + httpx clients), before FastAPI dispatches to the endpoint. Handlers do the actual work and Pydantic schemas serialise the response.

## Backend

### Layers

The backend follows a fairly conventional layering. Endpoints handle request validation and response serialisation, while the actual business logic lives in handlers organised by concern: `handler/database/` for per-entity CRUD, `handler/metadata/` for provider-specific normalisation, `handler/filesystem/` for I/O, and `handler/auth/` for the multi-method auth backend. Models are SQLAlchemy ORM, and adapters wrap the external APIs.

### Authentication

`HybridAuthBackend` walks methods in order of session cookie (looked up in Valkey), HTTP Basic (bcrypt), OAuth2 Bearer JWT (HS256), Client API Token (`rmm_...`, SHA-256 lookup), OIDC, kiosk mode if enabled. Token plaintext is never stored as we hash on creation and compare hashes on every request.

### Metadata providers

Each provider has a handler under `handler/metadata/` that normalises responses into a common shape. Priority is configurable in `config.yml` (`scan.priority.metadata`), where first match wins per field, with manual overrides on top.

Hashing can be platform-aware: `.chd` files pull their SHA1 values straight from the file header, PICO-8 cartridges (`.p8.png`) get a special-cased extractor, and the RetroAchievements per-platform algorithm runs through `rahasher.py`. Switch and PS3/4/5 skip hashing entirely, since those ROMs aren't reasonably hashable in the first place and have no TOSEC/No-Intro entries.

### Configuration

Environment variables (100+ of them, all listed in `env.template`) cover infrastructure concerns, while `config.yml` covers everything to do with the library, scanning, and emulator behaviour. The config is read, validated, and written back through the singleton `ConfigManager`.

### Background jobs

RQ workers run scheduled jobs (rescans, Switch TitleDB refresh, LaunchBox refresh, image-to-WebP conversion, RA progress sync, netplay cleanup) and manual tasks (`cleanup_missing_roms`, `cleanup_orphaned_resources`, `sync_folder_scan`). Each scheduled task is gated by an `ENABLE_SCHEDULED_*` env var and tunable via the matching `*_CRON`. Operator-side detail in [Scheduled Tasks](../administration/scheduled-tasks.md).

## Frontend

### Stack

The frontend is a Vue 3 SPA written in TypeScriptusing the Composition API and `<script setup>` syntax, bundled by Vite which gives HMR in development. The UI layer is Vuetify 3 (Material Design) topped with Tailwind CSS 4 for utility classes, and state lives in Pinia stores. Vue Router covers named routes across three layouts, while vue-i18n supplies translations for language packs. Live updates flow through `socket.io-client` for scan progress and netplay, and Mitt sits in the middle as a loose event bus, which is handy for triggering dialogs from anywhere in the component tree without having to thread refs through props.

### Generated types

TypeScript interfaces in `src/__generated__/` are produced from the backend OpenAPI spec by running `npm run generate`, and the stores and API services consume them directly, giving you type-safe end-to-end communication. Re-run the generator after any backend route or schema change so the frontend types stay in sync.

### Persistence

UI preferences live in localStorage and sync to `user.ui_settings` on the backend through the `useUISettings` composable, so a user's settings follow them across devices and browsers. Session data sits in Pinia in memory, and the Browser Cache API holds API responses when the _experimental_ opt-in cache layer is enabled.

### Layouts

Three layouts cover the routes:

- **Auth** (public): setup, login, password reset, register
- **Main** (authenticated): home, gallery, game details, scan, patcher, settings, admin
- **Console** (authenticated, gamepad/TV): `/console/*`

Permission-protected routes follow the scope model from [Users & Roles](../administration/users-and-roles.md): `/scan` and `/library-management` require `platforms.write`, `/client-api-tokens` requires `me.write`, and `/administration` requires `users.write`.

### Console Mode

A second SPA bundle aimed at TVs and gamepads is kept under `frontend/src/console/`. The input system is a stack-based bus with grid-based spatial navigation, gamepad polling runs in `requestAnimationFrame`, and the sound effects are synthesised on the fly through the Web Audio API rather than shipped as audio assets.

## Real-time

Two socket.io servers run side by side, both Valkey-backed so they horizontally scale across multiple replicas. `/ws` carries scan progress (`scan:update_stats`, `scan:log`, `scan:stop`) and general notifications, while `/netplay` handles room creation, joining, and peer message relay. The wire-level reference is in [WebSockets](websockets.md).

## Filesystem layout

```text
{ROMM_BASE_PATH}/                # Default: /romm
├── library/{platform_slug}/     # ROMs (roms/) and BIOS (bios/)
├── resources/roms/{rom_id}/     # Cached cover art + screenshots
├── assets/users/{user_id}/      # User saves, states, screenshots
└── config/config.yml            # YAML configuration
```

Production serves files via nginx `X-Accel-Redirect`. Dev mode (`DEV_MODE=true`) falls back to FastAPI's `FileResponse`, slower but no nginx in the loop.

## Observability

Sentry (opt-in via `SENTRY_DSN`) captures unhandled exceptions, tagged with `romm@{version}`. OpenTelemetry (opt-in) ships traces, metrics, and logs over OTLP. `GET /api/heartbeat` returns an aggregated health snapshot, safe to scrape from uptime monitors. Setup details in [Observability](../administration/observability.md).

## Where to start

If you're picking up your first issue, the patterns to mimic live in `backend/handler/` for backend work and in `frontend/src/components/` plus the relevant Pinia store for frontend work. Match the surrounding style. The hardest part of contributing isn't writing the change, it's threading it through the existing layers cleanly (see [Contributing](contributing.md) for process and [Development Setup](development-setup.md) to get a local env running).
