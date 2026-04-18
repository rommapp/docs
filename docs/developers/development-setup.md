---
title: Development Setup
description: Run RomM locally for development — Docker, manual, tests, lint.
---

# Development Setup

Two paths: **Docker** (recommended — matches production closely) or **manual** (edit Python on your host, faster iteration cycles).

If you're contributing, also read [Contributing](contributing.md).

## Option 1 — Docker

Simplest. One command brings up the whole stack.

### 1. Clone + mock the library

Get the code and create the minimal fixtures RomM expects at runtime:

```sh
git clone https://github.com/rommapp/romm.git
cd romm

mkdir -p romm_mock/library/roms/switch
touch   romm_mock/library/roms/switch/metroid.xci
mkdir -p romm_mock/resources romm_mock/assets romm_mock/config
touch    romm_mock/config/config.yml
```

### 2. `.env`

```sh
cp env.template .env
```

Then edit `.env` to set dev defaults:

```dotenv
ROMM_BASE_PATH=/app/romm
DEV_MODE=true
```

### 3. Build + bring up

```sh
docker compose build    # --no-cache to force a clean rebuild
docker compose up -d
```

That's it. RomM is on `http://localhost:3000`. Source mounts are live — edit backend or frontend code and changes reflect on the next request (backend) or instantly (frontend HMR).

## Option 2 — Manual

Faster iteration cycles than Docker if you're touching Python a lot.

### 1. Clone + mock the library

Same as Docker Option 1.

```sh
git clone https://github.com/rommapp/romm.git
cd romm

mkdir -p romm_mock/library/roms/switch
touch   romm_mock/library/roms/switch/metroid.xci
mkdir -p romm_mock/resources romm_mock/assets romm_mock/config
touch    romm_mock/config/config.yml

cp env.template .env
```

### 2. System dependencies

```sh
# Debian / Ubuntu
sudo apt install libmariadb3 libmariadb-dev libpq-dev
```

Adjust for your distro; the key libraries are the MariaDB connector and libpq for Postgres.

#### RAHasher (optional)

Only needed if you're working on RetroAchievements hash calculation. **Not supported on macOS — skip.**

```sh
git clone --recursive https://github.com/RetroAchievements/RALibretro.git
cd RALibretro
git checkout 1.8.0
git submodule update --init --recursive
sed -i '22a #include <ctime>' ./src/Util.h
make HAVE_CHD=1 -f ./Makefile.RAHasher
sudo cp ./bin64/RAHasher /usr/bin/RAHasher
cd ..
```

### 3. Python environment

RomM uses [uv](https://docs.astral.sh/uv/getting-started/installation/):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh

uv venv
source .venv/bin/activate
uv sync --all-extras --dev
```

### 4. Start supporting services

MariaDB and Redis come up via the dev compose file:

```sh
docker compose up -d
```

### 5. Run the backend

Alembic migrations run automatically on start.

```sh
cd backend
uv run python3 main.py
```

### 6. Frontend

In a second terminal:

```sh
cd frontend
# needs Node.js 24+ and npm >= 9
npm install
```

Symlink the mock `resources/` and `assets/` into the frontend's serving tree so uploaded-media URLs resolve during dev:

```sh
mkdir -p assets/romm
ln -s ../../romm_mock/resources assets/romm/resources
ln -s ../../romm_mock/assets    assets/romm/assets

npm run dev
```

Frontend is on `http://localhost:3000`; it proxies API calls through to the backend.

## Linting

RomM uses [Trunk](https://trunk.io) as a meta-linter — it wraps ruff, prettier, eslint, markdownlint, and a few others under one config.

```sh
curl https://get.trunk.io -fsSL | bash

trunk fmt       # auto-fix what it can
trunk check     # report what it can't
```

Trunk runs as a pre-commit hook automatically after install. Alternative install methods are in [the Trunk docs](https://docs.trunk.io/check/usage#install-the-cli).

!!! warning "CI blocks un-linted PRs"
    Trunk's check runs on every PR. If it fails, your PR can't merge — same rules as the maintainers.

## Tests

### One-time: create the test DB + user

```sh
docker exec -i romm-db-dev mariadb -uroot -p<root-password> < backend/romm_test/setup.sql
```

The password is whatever you set for `MARIADB_ROOT_PASSWORD` in `.env`.

### Run

Migrations run automatically before tests.

```sh
cd backend
uv run pytest                    # all tests
uv run pytest path/to/file.py    # one file
uv run pytest -vv                # verbose
uv run pytest -k scan            # match by name
```

## Useful dev URLs

| URL | Purpose |
| --- | --- |
| `http://localhost:3000` | Main UI |
| `http://localhost:3000/api/docs` | Swagger UI — try endpoints live |
| `http://localhost:3000/api/redoc` | ReDoc-rendered API reference |
| `http://localhost:3000/openapi.json` | OpenAPI spec — source of truth for client generators |
| `http://localhost:3000/api/heartbeat` | Health + config snapshot |

## Architecture at a glance

If you're new to the codebase, read [Architecture](architecture.md) for a high-level walkthrough, then come back here. The short version:

- `backend/` — FastAPI, SQLAlchemy, Alembic, RQ workers.
- `frontend/` — Vue 3 + Vuetify + Pinia + Vite. Separate `/console` SPA for TV/gamepad mode.
- `docker/` — nginx config (with `mod_zip`), entrypoint scripts, multi-stage Dockerfiles.
- `examples/` — reference compose files.

## Getting stuck

- The `#dev` channel on the [RomM Discord](https://discord.gg/romm) is the fastest unblock path.
- File an issue at [rommapp/romm](https://github.com/rommapp/romm/issues) if it's reproducible and you've got steps.
