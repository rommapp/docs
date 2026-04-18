---
title: Architecture
description: High-level walkthrough of the RomM codebase — backend, frontend, nginx, workers.
---

# Architecture

A walkthrough of how RomM is put together, aimed at first-time contributors. Enough to orient yourself before diving in.

## Repo layout

```text
rommapp/romm
├── backend/              # Python FastAPI application
├── frontend/             # Vue 3 + Vuetify SPA (main UI)
├── docker/               # nginx config, entrypoint, Dockerfiles
├── examples/             # Reference docker-compose.yml and config.yml
├── env.template          # Env var reference
└── pyproject.toml        # Backend Python deps
```

Key sub-directories:

- `backend/routers/` — FastAPI route definitions, one file per resource group.
- `backend/handlers/` — business logic (scan engine, metadata providers, auth).
- `backend/tasks/` — RQ job definitions (scheduled + manual + watcher tasks).
- `backend/config/` — Pydantic config schemas for `config.yml`.
- `backend/alembic/` — DB migrations.
- `backend/romm_test/` — test suite.
- `frontend/src/views/` — top-level Vue pages.
- `frontend/src/console/` — Console Mode SPA (separate entry).
- `frontend/src/stores/` — Pinia state stores.

## Runtime topology

A running RomM container hosts several cooperating processes:

```
┌─────────────────────────────────────────────────────────┐
│ docker container                                        │
│                                                         │
│  ┌───────┐   HTTP   ┌───────┐   python   ┌───────────┐  │
│  │ nginx │────────→│ gunicorn│──→│ FastAPI │           │
│  │ :8080 │          │  :5000  │   │ backend │           │
│  └───┬───┘          └─────────┘   └────┬────┘           │
│      │   static files              SQL │                │
│      │ (EmulatorJS,                    │                │
│      │  Ruffle, SPA)                   ↓                │
│      │                           ┌─────────┐            │
│      │                           │ MariaDB │(external)  │
│      ↓                           │ (replica)│           │
│  ┌──────┐                        └─────────┘            │
│  │ serve│                                               │
│  │ /library│←── bind mount from host                    │
│  │ /assets │    read/write                              │
│  │ /resources│                                          │
│  └──────┘                                               │
│                                                         │
│  ┌────────┐            ┌────────┐                       │
│  │ RQ     │←──────────→│ Redis  │                       │
│  │ workers│   tasks    │ (embedded or external)          │
│  └────────┘            └────────┘                       │
└─────────────────────────────────────────────────────────┘
```

### The parts

- **nginx** — listens on `8080`. Serves static assets (the SPA bundle, EmulatorJS core files, Ruffle, cover images). Proxies API + WebSocket traffic to gunicorn. Streams large downloads via `mod_zip`.
- **gunicorn** — the Python WSGI server, running the FastAPI app. Multiple worker processes; `WEB_SERVER_CONCURRENCY` tunes count.
- **FastAPI backend** — routes, handlers, DB access via SQLAlchemy, Redis for sessions + cache + queue.
- **RQ workers** — separate process(es) that pop jobs off Redis queues and run them. Scans, metadata syncs, cleanup tasks.
- **Redis / Valkey** — in-container by default (full image), externalisable.
- **MariaDB / Postgres / MySQL / SQLite** — always external (or a separate container).

## Request lifecycle

### Browsing the library (GET `/api/roms`)

1. Browser sends request → reverse proxy → nginx.
2. nginx forwards to gunicorn → FastAPI → `backend/routers/roms.py`.
3. Handler queries MariaDB via SQLAlchemy.
4. Response serialised, returned.

Simple. Same flow for every non-WebSocket API call.

### Uploading a ROM (POST `/api/roms/upload/*`)

1. Browser → nginx. nginx buffers up to `client_max_body_size`.
2. gunicorn → FastAPI → `backend/routers/roms_upload.py`.
3. Handler writes chunks to a temp path, assembles on complete.
4. Moved into place under `/romm/library`.
5. DB entry created.
6. Socket.IO emits `rom:created`.

Large uploads go through the chunked-upload flow for a reason: gunicorn's per-request memory ceiling would otherwise be an issue.

### Scanning

1. Trigger: UI button, `/api/tasks/run/scan`, scheduled cron, or watcher event.
2. Handler enqueues an RQ job.
3. Worker pops job, runs `handlers/scan.py`:
    - Walks filesystem.
    - Hashes files.
    - Calls metadata providers in parallel.
    - Writes to DB.
4. Emits `scan:progress` and `scan:log` via Socket.IO during execution.
5. Emits `scan:complete` when done.

## Frontend architecture

### Main UI (`frontend/src/`)

- **Vue 3 + Composition API**.
- **Vuetify 3** for UI components.
- **Vite** for build + dev server with HMR.
- **Pinia** for state management — one store per resource family (auth, roms, platforms, collections, etc.).
- **vue-i18n** for localisation. Translations in `src/locales/<locale>/`.
- **socket.io-client** for live updates.

Router in `src/plugins/router.ts`. Top-level views in `src/views/`.

### Console Mode SPA (`frontend/src/console/`)

Separate SPA, compiled as a second bundle. Entry point at `/console`. Built with the same Vue + Pinia + i18n stack but:

- Own router with `/console` namespace.
- Own component library tuned for gamepad navigation (bigger targets, spatial focus, SFX).
- Own theme in `src/console/styles/`.

## Background work

RQ has three priority queues:

- **high** — user-triggered scans, manual tasks. Get fast.
- **default** — scheduled nightlies, sync operations.
- **low** — cleanup, image conversion. Run when the system's idle.

All queues share the same worker pool. Jobs are Redis-backed, so restarting RomM doesn't lose in-flight work (appendonly needs to be on — see [Redis or Valkey](../install/redis-or-valkey.md)).

## Auth

Session state in Redis. Passwords bcrypt-hashed in the DB. JWT for OAuth2 bearer tokens.

OIDC handled via `authlib` on the backend. Session cookies issued after successful OIDC callback; from there, it's a regular session.

Client API Tokens are stored as hash-only in the DB (we never store the plaintext token after creation). A token is validated by hashing the presented bearer and comparing.

## Observability

- **Sentry** (opt-in) — unhandled exceptions.
- **OpenTelemetry** (opt-in) — traces, metrics, logs via OTLP.
- **`/api/heartbeat`** — aggregated health snapshot.

See [Observability](../administration/observability.md).

## Why these choices

- **FastAPI**: modern, async, auto-OpenAPI. Good fit for the API-shape of the app.
- **Vue + Vuetify**: fast, componenty, looks decent out of the box.
- **MariaDB** as default: solid, familiar, works everywhere.
- **RQ** not Celery: simpler, Redis-native, less operational overhead. Works fine at RomM's scale.
- **Socket.IO**: pragmatic. Raw WebSocket would be leaner but SIO's client ecosystem is worth the overhead.

## Contributing

See [Contributing](contributing.md) for the process + style expectations.

For large changes, read the relevant handler in `backend/handlers/` first — the patterns there will guide what you write.

## See also

- [Development Setup](development-setup.md) — get a local env running.
- [API Reference](api-reference.md) — what the backend exposes.
- [WebSockets](websockets.md) — Socket.IO endpoints in detail.
- [Configuration File](../reference/configuration-file.md) — `config.yml` schema.
