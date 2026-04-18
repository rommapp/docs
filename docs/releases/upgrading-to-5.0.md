---
title: Upgrading to 5.0
description: Migrate from RomM 4.x to 5.0 — breaking changes, env var renames, pre-flight checklist, and rollback.
---

# Upgrading to 5.0

Migration guide for **RomM 4.x → 5.0**. If you're on 2.x or earlier, upgrade to 3.x first via [Upgrading to 3.0](upgrading-to-3.0.md), then come back here.

!!! danger "Read this entire page before upgrading"
    5.0 is a major release with schema migrations and a handful of breaking changes. Skipping the pre-flight checklist will lose data or break your instance.

!!! note "This guide is finalised at 5.0 GA"
    Some sections below reference exact env-var renames and schema changes that will be confirmed against the final 5.0.0 source tag. If you're reading this before 5.0 GA, treat it as a structural outline — the commands are correct, specific rename lists will be filled in as the release tag is cut.

## What changes in 5.0

### Summary

- **Schema migration** — Alembic runs automatically on startup. Irreversible without a backup.
- **New env vars**, some renamed (see [Env var migration table](#env-var-migration-table)).
- **`config.yml` gains new sections** — `scan.region`, `scan.language`, `scan.media`, `scan.gamelist.export`, `scan.pegasus.export`, `emulatorjs.*`, `filesystem.firmware_folder`. Old settings keep working untouched.
- **Image tags add `:slim` variants** — no change to existing `:latest` / `:5.0.0`.
- **Docs URL structure** — every old URL redirects automatically. External links continue working.

### Big new features

Highlights only — full list in [What's New in 5.0](../getting-started/what-is-new-in-5.md):

- Console Mode (`/console` — TV/gamepad UI).
- Smart and Virtual Collections.
- ROM Patcher.
- Netplay with ICE servers.
- PWA install.
- 19 locales.
- Device Sync protocol (bidirectional push-pull for handhelds).
- Client API Tokens with device pairing.
- OIDC role mapping via claims.
- Expanded metadata providers: TheGamesDB, Libretro, gamelist.xml importer.
- OpenTelemetry export.

## Pre-flight checklist

**Do not skip.**

### 1. Read

- This whole page.
- [What's New in 5.0](../getting-started/what-is-new-in-5.md).
- The release's [GitHub Release notes](https://github.com/rommapp/romm/releases).

### 2. Check you're on a recent 4.x

5.0's migrations assume you've already run the 4.x migrations. From a 4.7 or 4.8 baseline is ideal. If you're on 3.x:

1. Upgrade to the latest 4.x first (`rommapp/romm:4.8.1` at time of writing).
2. Verify the instance works.
3. Then upgrade to 5.0.

Don't jump 3.x → 5.0 in one step.

### 3. Back up

See [Backup & Restore](../install/backup-and-restore.md). At minimum:

```sh
# MariaDB
docker exec romm-db mariadb-dump --user=romm-user --password=$DB_PASSWD \
  --single-transaction --databases romm > romm-db-pre-5.0.sql

# or Postgres
docker exec romm-db pg_dump --username=romm-user --dbname=romm > romm-db-pre-5.0.sql

# Assets + config
rsync -a /path/to/assets/ /backup/romm/assets-pre-5.0/
rsync -a /path/to/config/ /backup/romm/config-pre-5.0/
```

Don't skip this. "It's a minor upgrade" isn't a thing for a major version.

### 4. Pin the current version

Before pulling 5.0, change your `docker-compose.yml` to pin the old version explicitly so you can roll back:

```yaml
image: rommapp/romm:4.8.1   # whatever you're actually on
```

Commit this to version control if you track your compose file. Saves guesswork on rollback.

### 5. Block access while you upgrade

Optional but recommended for shared instances — take RomM offline for ~5 minutes:

```sh
# Return 503 at the reverse proxy while upgrading
```

Prevents users hitting mid-migration state.

## Upgrade steps

### 1. Pull the new image

```sh
docker pull rommapp/romm:5.0.0
```

Or pick the slim variant:

```sh
docker pull rommapp/romm:5.0.0-slim
```

### 2. Update your compose file

Edit `docker-compose.yml`:

- Change the image tag to `rommapp/romm:5.0.0` (or `:5.0.0-slim`).
- Add any new env vars relevant to your setup from the [migration table](#env-var-migration-table).
- Rename any renamed env vars.
- Double-check volumes are still correct.

### 3. Bring it up

```sh
docker compose up -d
docker compose logs -f romm
```

What to watch for:

- **Alembic migrations running** — lines prefixed `INFO [alembic.runtime.migration]`. Takes anywhere from seconds (small libraries) to a couple minutes (very large ones).
- **`Application startup complete.`** — RomM is healthy.
- **`Watcher started.`** — filesystem watcher up (if enabled).
- **ERROR lines** — bad; go to [Rollback](#rollback).

### 4. Smoke-test

Don't trust the migration until you've verified:

- Log in as an Admin.
- **Administration → Server Stats** — counts look reasonable; no massive loss.
- Open a platform with lots of games; check a few games have metadata.
- Open a game's details — Personal tab shows your rating / playtime if you had any.
- Check **Administration → Users** — your accounts are intact.
- Run a **Quick** scan — should complete cleanly in a few seconds.
- (If you had OIDC) log out, log in via OIDC — should pick up `OIDC_CLAIM_ROLES` if configured.

## Env var migration table

| 4.x name | 5.0 name | Change |
| --- | --- | --- |
| `SCREENSCRAPER_USER` | `SCREENSCRAPER_USER` | No change. |
| `IGDB_CLIENT_ID` | `IGDB_CLIENT_ID` | No change. |
| _(new in 5.0)_ | `ALLOW_PUBLIC_REGISTRATION` | Opt-in public signup. Off by default. |
| _(new in 5.0)_ | `INVITE_TOKEN_DAYS` | Invite link expiry (days). Default 30. |
| _(new in 5.0)_ | `OIDC_CLAIM_ROLES` | Which claim to read for role mapping. |
| _(new in 5.0)_ | `OIDC_ROLE_VIEWER` / `OIDC_ROLE_EDITOR` / `OIDC_ROLE_ADMIN` | Map OIDC group names to RomM roles. |
| _(new in 5.0)_ | `ENABLE_NETPLAY` | Toggle Netplay (default on). |
| _(new in 5.0)_ | `WATCHER_ENABLED` | Filesystem watcher (default on). |
| _(new in 5.0)_ | `WATCH_EXTENSIONS_ONLY` | Watcher filters by extension. |
| _(new in 5.0)_ | `RESCAN_ON_FILESYSTEM_CHANGE` / `RESCAN_ON_FILESYSTEM_CHANGE_DELAY` | Watcher debounce. |
| _(new in 5.0)_ | `OTEL_ENABLED` | Opt into OpenTelemetry export. |
| _(new in 5.0)_ | `SSH_PRIVATE_KEY_PATH` | Path to SSH key used by Push-Pull Device Sync. |
| _(new in 5.0)_ | `TGDB_API_ENABLED` | Enable TheGamesDB as a metadata source. |
| _(new in 5.0)_ | `RETROACHIEVEMENTS_SYNC_INTERVAL_CRON` / `NETPLAY_CLEANUP_INTERVAL_CRON` / `PUSH_PULL_SYNC_INTERVAL_CRON` / `IMAGE_CONVERSION_INTERVAL_CRON` / `SWITCH_TITLEDB_FETCH_INTERVAL_CRON` | New scheduled-task cron controls. |

Full list in [Environment Variables](../reference/environment-variables.md). The reference page is autogenerated from the upstream `env.template`, so it stays correct even as more vars land in 5.x patches.

## `config.yml` changes

`config.yml` gains new sections; everything else stays backwards compatible.

- **`scan.region`** — region preference order (array).
- **`scan.language`** — language preference order (array).
- **`scan.media`** — which media types to fetch (`[box2d, screenshot, manual]`, etc.).
- **`scan.gamelist.export`** + **`scan.gamelist.media.*`** — export gamelist.xml for ES-DE/Batocera.
- **`scan.pegasus.export`** — export metadata.pegasus.txt for Pegasus.
- **`filesystem.firmware_folder`** — override the `bios` folder name.
- **`emulatorjs.netplay.ice_servers`** — STUN/TURN for Netplay.
- **`emulatorjs.settings`** / **`emulatorjs.controls`** — per-core emulator config and button mappings.
- **`emulatorjs.cache_limit`** / **`emulatorjs.disable_batch_bootup`** / **`emulatorjs.disable_auto_unload`**.

Full schema: [Configuration File](../reference/configuration-file.md).

## Docs URL changes

The docs site restructured in 5.0. Every old URL redirects to its new home:

- `/latest/Getting-Started/Quick-Start-Guide/` → `/latest/getting-started/quick-start/`
- `/latest/System-Setup/Synology-Setup-Guide/` → `/latest/install/synology/`
- `/latest/Usage/UserManagement/` → `/latest/administration/users-and-roles/`
- `/latest/OIDC-Guides/OIDC-Setup-With-Keycloak/` → `/latest/administration/oidc/keycloak/`

And so on — every page in the 4.x IA is covered. External links in forum posts, blog articles, issue threads, and Discord messages keep working. Internal bookmarks to `/latest/<old-pascal-case>/<old-page>/` hit a 301 to the new slug automatically.

## Rollback

If something's clearly broken after the upgrade:

### 1. Stop the stack

```sh
docker compose down
```

### 2. Revert the image tag

Edit `docker-compose.yml` — change `rommapp/romm:5.0.0` back to whatever you were on (`rommapp/romm:4.8.1`).

### 3. Restore the DB

```sh
# MariaDB / MySQL
docker compose up -d romm-db                  # DB only
docker exec -i romm-db mariadb --user=root --password=$ROOT_PW romm \
  < romm-db-pre-5.0.sql

# Postgres
docker compose up -d romm-db
docker exec -i romm-db psql --username=romm-user --dbname=romm \
  < romm-db-pre-5.0.sql
```

### 4. Restore assets + config

```sh
rsync -a /backup/romm/assets-pre-5.0/ /path/to/assets/
rsync -a /backup/romm/config-pre-5.0/ /path/to/config/
```

### 5. Start the old version

```sh
docker compose up -d
```

Open a bug report on [GitHub](https://github.com/rommapp/romm/issues) with:

- Your previous version.
- Whatever you saw in `docker logs romm` during the 5.0 startup.
- Your deployment (Docker Compose, Unraid, K8s, etc.).

## Common upgrade issues

### Migrations hang

Watch `docker logs -f romm`. If Alembic is still running, it's still running — large DBs take a while. If it's been more than 10 minutes with no progress, something's wrong. Check for:

- DB connection issues (`docker logs romm-db`).
- Out-of-memory kills (`dmesg | grep -i oom`).
- Missing new env vars that migrations rely on.

### WebSockets fail after upgrade

If you're behind a reverse proxy, the upgrade shouldn't change anything — but it's a good moment to verify the proxy forwards `Upgrade: websocket` properly. See [Reverse Proxy](../install/reverse-proxy.md).

### OIDC users lose role, come back as Viewer

5.0 introduces `OIDC_CLAIM_ROLES`. Before 5.0, OIDC users were always Viewer. After 5.0, if you set `OIDC_CLAIM_ROLES`, roles are reassigned on **every login** based on IdP claims. If your IdP doesn't emit the expected claim yet, every OIDC user gets demoted to Viewer.

Fix: either don't set `OIDC_CLAIM_ROLES` (keeps 4.x behaviour), or wire the claim on the IdP side before enabling the mapping.

See [OIDC Setup → Role mapping](../administration/oidc/index.md#role-mapping-50).

### Scheduled tasks stop firing

5.0 renamed several cron env vars. Check [Environment Variables](../reference/environment-variables.md) and update your env to the new names — otherwise the old cron expressions are ignored and tasks run on defaults (or not at all, if you previously disabled them).

## After the upgrade

Once everything's stable:

- Pin your image to `rommapp/romm:5.0.0` in version control.
- Update your uptime monitor's heartbeat endpoint — still `/api/heartbeat`, but now exposes more info (see [Observability](../administration/observability.md)).
- Take a fresh backup of the post-migration state. You want a known-good 5.0 snapshot, not just the pre-5.0 one.
- Explore the new stuff in [What's New in 5.0](../getting-started/what-is-new-in-5.md).
