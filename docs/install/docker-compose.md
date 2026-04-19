---
title: Docker Compose
description: Canonical Docker Compose reference for a production RomM 5.0 deployment.
---

# Docker Compose

The canonical way to run RomM is with Docker Compose, and this page describes the full reference stack. The shorter happy-path walkthrough lives in [Quick Start](../getting-started/quick-start.md).

The RomM stack has three parts:

1. **`romm`**: the application container with Valkey embedded.
2. **A database**: MariaDB by default but MySQL and PostgreSQL are also supported. See [Databases](databases.md) for details and driver-specific notes.

## Reference `docker-compose.yml`

```yaml
--8<-- "quick-start.docker-compose.yml"
```

## Service reference

### `romm`

| Field        | Value                 | Notes                                                                                                                                               |
| ------------ | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image`      | `rommapp/romm:latest` | Or `ghcr.io/rommapp/romm:latest`; pin to a specific tag (`5.0.0`) for production, and see [Image Variants](image-variants.md) for `slim` vs `full`. |
| `ports`      | `80:8080`             | Container listens on `8080`; expose through a reverse proxy in production (see [Reverse Proxy](reverse-proxy.md)).                                  |
| `volumes`    | see below             | RomM writes to four distinct paths inside the container.                                                                                            |
| `depends_on` | `romm-db` (healthy)   | RomM exits on startup if the DB isn't reachable.                                                                                                    |

#### Volumes

| Path inside container | Purpose                                                | Backup priority                                      |
| --------------------- | ------------------------------------------------------ | ---------------------------------------------------- |
| `/romm/library`       | Your ROM files, typically mounted **read-only**.       | No: this is your source data, back it up separately. |
| `/romm/assets`        | User uploads: saves, states, uploaded screenshots.     | **Critical**, back this up with your DB.             |
| `/romm/resources`     | Metadata assets fetched from IGDB, ScreenScraper, etc. | Low, and can be re-downloaded on a rescan.           |
| `/romm/config`        | Holds `config.yml`.                                    | **Critical**, hand-tuned config, back it up.         |

See [Backup & Restore](backup-and-restore.md) for the full procedure.

#### Core environment variables

Minimal set: see the [Environment Variables reference](../reference/environment-variables.md) for the complete list.

| Variable                                     | What it does                                                            |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| `ROMM_AUTH_SECRET_KEY`                       | (Required) Generate the JWT signing secret with `openssl rand -hex 32`. |
| `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWD` | Database connection.                                                    |
| `ROMM_DB_DRIVER`                             | One of `mariadb` (default), `mysql`, or `postgresql`.                   |
| `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWD`   | Only set if you're using an external Redis/Valkey instance.             |
| Metadata provider creds                      | See [Metadata Providers](../administration/metadata-providers.md).      |

### `romm-db` (MariaDB)

| Field         | Value                                           | Notes                                                 |
| ------------- | ----------------------------------------------- | ----------------------------------------------------- |
| `image`       | `mariadb:latest`                                | Pin to a major version (`mariadb:11`) for production. |
| `volumes`     | `mysql_data:/var/lib/mysql`                     | Back this up, since it's your entire catalogue.       |
| `healthcheck` | `healthcheck.sh --connect --innodb_initialized` | RomM waits for this.                                  |

The default compose file uses MariaDB because it requires no extra driver configuration. To use PostgreSQL, swap the image for `postgres:16`, set `ROMM_DB_DRIVER=postgresql`, and point `DB_PORT` at `5432`: see [Databases](databases.md) for the full swap.

## Production hardening

The quick-start compose file is functional but not production-ready. Before exposing RomM to the internet:

- **Pin image tags**: `rommapp/romm:latest` moves, so use `rommapp/romm:5.0.0` (or whatever release you're on).
- **Use a reverse proxy with HTTPS**: the built-in nginx listens on `8080` and terminates plain HTTP, so put Traefik, Caddy, or nginx in front with TLS (see [Reverse Proxy](reverse-proxy.md)).
- **Set a non-default `MARIADB_ROOT_PASSWORD`**, and don't reuse it for `MARIADB_PASSWORD`.
- **Mount the library read-only** unless you need RomM to write into it: `- /path/to/library:/romm/library:ro`.
- **Use Docker secrets for credentials** if your orchestrator supports them: RomM recognises `ROMM_AUTH_SECRET_KEY_FILE` for loading the secret from a file mount.
- **Enable backups**: at minimum, daily `mysqldump` + rsync of `/romm/assets` and `/romm/config` (see [Backup & Restore](backup-and-restore.md)).

## Updating

```sh
docker compose pull
docker compose up -d
```

Alembic migrations run automatically on startup but read the [release notes](../releases/index.md) before every major-version bump. The 4.x → 5.0 jump in particular has breaking changes, covered in [Upgrading to 5.0](../releases/upgrading-to-5.0.md).
