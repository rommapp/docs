---
title: Development Setup
description: Run RomM locally for development
---

# Development Setup

There are two paths to a working dev environment, and which one suits you depends on how often you'll be touching Python:

- **Docker** (recommended): one command brings up the whole stack, and the result matches production closely.
- **Manual**: edit Python directly on your host for faster iteration when you're elbow-deep in the backend.

If you're planning to contribute changes back, also read [Contributing](contributing.md) before opening a PR.

## Option 1: Docker

The simplest path: everything runs in containers, and source mounts let you edit code without rebuilding the image.

### 1. Clone and mock the library

Get the code and create the minimal fixtures RomM expects at runtime:

```sh
git clone https://github.com/rommapp/romm.git
cd romm

mkdir -p romm_mock/library/roms/switch
touch   romm_mock/library/roms/switch/metroid.xci
mkdir -p romm_mock/resources romm_mock/assets romm_mock/config
touch    romm_mock/config/config.yml
```

### 2. Configure `.env`

```sh
cp env.template .env
```

Edit `.env` for dev defaults:

```dotenv
ROMM_BASE_PATH=/app/romm
DEV_MODE=true
```

### 3. Build and bring up

```sh
docker compose build    # add --no-cache to force a clean rebuild
docker compose up -d
```

That's it — RomM is up at `http://localhost:3000`, and the source mounts are live so backend changes reflect on the next request and frontend changes are HMR-instant.

## Option 2: Manual

Faster iteration than Docker when you're spending most of your time in the Python code, since you skip the container layer.

### 1. Clone and mock the library

Same as Docker step 1:

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

Adjust for your distro. The MariaDB connector and libpq are the two non-negotiables.

### 3. RAHasher (optional)

Only needed if you're working on RetroAchievements hash calculation. **Not supported on macOS — skip it.**

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

### 4. Python environment

RomM uses [uv](https://docs.astral.sh/uv/getting-started/installation/):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh

uv venv
source .venv/bin/activate
uv sync --all-extras --dev
```

### 5. Start supporting services

MariaDB and Valkey come up via the dev compose file:

```sh
docker compose up -d
```

### 6. Run the backend

Alembic migrations run automatically on start.

```sh
cd backend
uv run python3 main.py
```

### 7. Frontend

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

The frontend runs at `http://localhost:3000` and proxies API calls through to the backend, so you only have one URL to remember.

## Linting

RomM uses [Trunk](https://trunk.io) as a meta-linter, wrapping ruff, prettier, eslint, markdownlint, and a few others under one config.

```sh
curl https://get.trunk.io -fsSL | bash

trunk fmt       # auto-fix what it can
trunk check     # report what it can't
```

Trunk runs as a pre-commit hook automatically after install. Other install paths are in [the Trunk docs](https://docs.trunk.io/check/usage#install-the-cli).

<!-- prettier-ignore -->
!!! warning "CI blocks un-linted PRs"
    Trunk's check runs on every PR. If it fails, your PR can't merge. Same rules as the maintainers — no exceptions.

## Tests

### One-time test DB setup

```sh
docker exec -i romm-db-dev mariadb -uroot -p<root-password> < backend/romm_test/setup.sql
```

The password is whatever you set for `MARIADB_ROOT_PASSWORD` in `.env`.

### Running tests

Migrations run automatically before tests.

```sh
cd backend
uv run pytest                    # all tests
uv run pytest path/to/file.py    # one file
uv run pytest -vv                # verbose
uv run pytest -k scan            # match by name
```

## Useful dev URLs

| URL                                   | Purpose                                            |
| ------------------------------------- | -------------------------------------------------- |
| `http://localhost:3000`               | Main UI                                            |
| `http://localhost:3000/api/docs`      | Swagger UI: try endpoints live                     |
| `http://localhost:3000/api/redoc`     | ReDoc-rendered API reference                       |
| `http://localhost:3000/openapi.json`  | OpenAPI spec: source of truth for client generators|
| `http://localhost:3000/api/heartbeat` | Health + config snapshot                           |

## Architecture at a glance

If you're new to the codebase, [Architecture](architecture.md) is the proper walkthrough. The short version:

- `backend/` — FastAPI, SQLAlchemy, Alembic migrations, and the RQ workers
- `frontend/` — Vue 3 with Vuetify, Pinia, and Vite, plus a separate `/console` SPA for TV and gamepad mode
- `docker/` — nginx config (with `mod_zip`), entrypoint scripts, and the multi-stage Dockerfiles
- `examples/` — reference compose files you can crib from

## Getting unstuck

The `#dev` channel on the [RomM Discord](https://discord.gg/romm) is the fastest path to unblock yourself. For reproducible bugs with clear repro steps, file an issue at [rommapp/romm](https://github.com/rommapp/romm/issues) instead.
