---
title: Databases
description: Supported database drivers for RomM, connection strings, and recommendations.
---

# Databases

RomM uses SQLAlchemy + Alembic for persistence. Four drivers are supported; pick based on what you already run.

| Driver | `ROMM_DB_DRIVER` | Image | Default port | Notes |
| --- | --- | --- | --- | --- |
| **MariaDB** (default, recommended) | `mariadb` | `mariadb:11` | `3306` | What the reference compose uses. Well-tested. |
| **MySQL** | `mysql` | `mysql:8` | `3306` | Largely interchangeable with MariaDB for RomM. |
| **PostgreSQL** | `postgresql` | `postgres:16` | `5432` | Supported. Use if you already run Postgres. |
| **SQLite** | `sqlite` | _(file on disk)_ | n/a | Dev/tiny deployments only. Not recommended for anything multi-user or larger than a few hundred games. |

RomM runs Alembic migrations automatically on startup; no manual step when upgrading.

## MariaDB (default)

This is what the [reference Compose](docker-compose.md) sets up. No extra config beyond filling in the passwords.

```yaml
services:
  romm:
    environment:
      - ROMM_DB_DRIVER=mariadb  # optional; this is the default
      - DB_HOST=romm-db
      - DB_PORT=3306
      - DB_NAME=romm
      - DB_USER=romm-user
      - DB_PASSWD=<strong-password>

  romm-db:
    image: mariadb:11
    environment:
      - MARIADB_ROOT_PASSWORD=<separate-strong-password>
      - MARIADB_DATABASE=romm
      - MARIADB_USER=romm-user
      - MARIADB_PASSWORD=<same-as-DB_PASSWD>
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      start_period: 30s
      interval: 10s
      timeout: 5s
      retries: 5
```

## MySQL

Identical compose to MariaDB, but swap the image and the healthcheck:

```yaml
services:
  romm:
    environment:
      - ROMM_DB_DRIVER=mysql
      - DB_HOST=romm-db
      - DB_PORT=3306
      - DB_NAME=romm
      - DB_USER=romm-user
      - DB_PASSWD=<strong-password>

  romm-db:
    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=<separate-strong-password>
      - MYSQL_DATABASE=romm
      - MYSQL_USER=romm-user
      - MYSQL_PASSWORD=<same-as-DB_PASSWD>
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## PostgreSQL

```yaml
services:
  romm:
    environment:
      - ROMM_DB_DRIVER=postgresql
      - DB_HOST=romm-db
      - DB_PORT=5432
      - DB_NAME=romm
      - DB_USER=romm-user
      - DB_PASSWD=<strong-password>

  romm-db:
    image: postgres:16
    environment:
      - POSTGRES_DB=romm
      - POSTGRES_USER=romm-user
      - POSTGRES_PASSWORD=<same-as-DB_PASSWD>
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U romm-user -d romm"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## SQLite (not recommended)

Set `ROMM_DB_DRIVER=sqlite`. The DB file lives at `{ROMM_BASE_PATH}/database`. No separate container required; useful for a laptop demo or a one-user install on a low-power box. Don't use this for anything you care about:

- No concurrent writers → scans and API calls block each other.
- The file can corrupt if the container is killed mid-write.
- Migrating to MariaDB/Postgres later requires a dump/reload.

## Extra connection parameters

`DB_QUERY_JSON` takes a JSON blob of extra parameters appended to the connection string. Useful for enabling TLS to an external DB, setting a connection timeout, or hitting a non-default port:

```yaml
environment:
  - DB_QUERY_JSON={"ssl": "true", "connect_timeout": "5"}
```

Exact keys depend on the driver; see SQLAlchemy / the driver's docs.

## Which should I pick?

- **Sticking with defaults?** MariaDB. That's what the reference compose uses and what the team tests against.
- **Already run Postgres?** Postgres. No reason to add a second DB engine.
- **Single-user laptop demo?** SQLite is fine; upgrade before adding anyone else.
- **External managed DB?** Any of MariaDB / MySQL / Postgres. Point `DB_HOST` at it and configure TLS via `DB_QUERY_JSON`.

Don't switch DB drivers on a running install without a plan; migrating the data requires a dump + reload, covered in [Backup & Restore](backup-and-restore.md).
