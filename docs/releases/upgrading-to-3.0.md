---
title: Upgrading to 3.0
description: Historical migration guide for 2.x → 3.0: SQLite drop, auth required, Redis built-in, config folder mount, assets volume.
---

# Upgrading to 3.0

!!! info "This is a historical guide"
    RomM 3.0 shipped a while ago. If you're on 2.x, still use this page. If you're on 3.x / 4.x, see [Upgrading to 5.0](upgrading-to-5.0.md).

Version 3.0 introduced several breaking changes aimed at improving performance and unlocking new features (EmulatorJS, in-browser saves/states). Read this entire page before pulling the new image. Skipping steps will make RomM inaccessible or unresponsive.

All the changes below are reflected in the example [docker-compose.yml](https://github.com/rommapp/romm/blob/master/examples/docker-compose.example.yml), which was significantly simplified in 3.0.

## Dropped SQLite support

SQLite was removed because of ongoing engineering issues. MariaDB is stabler and the only supported default. If you were on SQLite, RomM will auto-migrate your data to MariaDB, **but you need to make the following changes before upgrading**.

In your environment variables, set `ROMM_DB_DRIVER` to `mariadb` (or drop the variable entirely, it's no longer required) and add:

```yaml
environment:
  - DB_HOST=mariadb
  - DB_PORT=3306
  - DB_NAME=romm           # matches MYSQL_DATABASE in mariadb
  - DB_USER=romm-user      # matches MYSQL_USER
  - DB_PASSWD=<password>   # matches MYSQL_PASSWORD
```

Set up the MariaDB container using the [reference compose](../install/docker-compose.md).

## Authentication is now required

To support EmulatorJS, save/state management, and multi-user features, 3.0 requires authentication. If you were running with auth disabled, remove `ROMM_AUTH_ENABLED` and add:

```yaml
environment:
  - ROMM_AUTH_SECRET_KEY=<generate with `openssl rand -hex 32`>
```

We know this breaks the "unrestricted sharing" pattern some users relied on. See [Kiosk Mode](../administration/authentication.md#kiosk-mode) for a read-only anonymous-access option that ships with RomM.

## Redis is built in

The 2.x "experimental Redis" add-on container is gone. RomM ships with Redis internally. Remove the external Redis container and these environment variables:

```yaml
# Remove:
# - ENABLE_EXPERIMENTAL_REDIS
# - REDIS_HOST
# - REDIS_PORT
```

If you want an external Redis instance anyway (recommended for production), keep `REDIS_HOST` / `REDIS_PORT`. See [Redis or Valkey](../install/redis-or-valkey.md).

## Configuration folder

`config.yml` is now mounted via a **config folder**, not a single file mount.

Place your existing `config.yml` inside a directory and bind that directory to `/romm/config`:

```yaml
volumes:
  - /path/to/config:/romm/config
```

Updated example: [config.example.yml](https://github.com/rommapp/romm/blob/master/examples/config.example.yml). See also [Configuration File](../reference/configuration-file.md).

## New `/romm/assets` volume

3.0 introduced save, state, and screenshot management. Uploads land in `/romm/assets` inside the container, so mount a host path so they persist:

```yaml
volumes:
  - /path/to/assets:/romm/assets
```

Put this next to the folder you mount as `/romm/library` so all RomM-owned data stays together.

## After the upgrade

- Visit the web UI. You'll see a Setup Wizard if you had auth disabled previously. Complete it to create the first admin.
- Run a scan to re-match any games that lost metadata during the SQLite → MariaDB migration.
- Start using saves/states. They'll live under `/romm/assets` from now on.

## Rollback

If something breaks:

1. Restore your old `docker-compose.yml` / env file.
2. Restore your SQLite DB file backup (if you were on SQLite).
3. Pull the 2.x image tag explicitly (`rommapp/romm:2.x.y`).
4. `docker compose up -d`.

Going forward, the 3.x / 4.x / 5.x chain of migrations is documented in their respective guides. Start with [Upgrading to 5.0](upgrading-to-5.0.md) once you're on 3.x.
