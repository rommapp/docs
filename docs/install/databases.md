---
title: Databases
description: Supported database drivers
---

# Databases

RomM uses SQLAlchemy + Alembic for persistence. Three drivers are supported, so pick based on what you already run.

| Driver                             | `ROMM_DB_DRIVER` | Image         | Default port | Notes                                          |
| ---------------------------------- | ---------------- | ------------- | ------------ | ---------------------------------------------- |
| **MariaDB** (default, recommended) | `mariadb`        | `mariadb:11`  | `3306`       | What the reference compose uses. Well-tested.  |
| **MySQL**                          | `mysql`          | `mysql:8`     | `3306`       | Largely interchangeable with MariaDB for RomM. |
| **PostgreSQL**                     | `postgresql`     | `postgres:16` | `5432`       | Use if you already run Postgres.               |

## MariaDB (default)

This is what the [reference Compose](../getting-started/quick-start.md) sets up. No extra config beyond filling in the passwords.

```yaml
services:
    romm:
        environment:
            - ROMM_DB_DRIVER=mariadb
            - DB_HOST=romm-db
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

Identical compose to MariaDB but swap the image and the healthcheck:

```yaml
services:
    romm:
        environment:
            - ROMM_DB_DRIVER=mysql
            - DB_PORT=3306
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

## Binary logging and trigger privileges

RomM's migrations create triggers on the `roms` table. MariaDB and MySQL refuse trigger DDL when binary logging is enabled and the connecting user lacks `SUPER`, so the container aborts during startup with:

```text
sqlalchemy.exc.OperationalError: (mariadb.OperationalError) You do not have the SUPER
privilege and binary logging is enabled (you *might* want to use the less safe
log_bin_trust_function_creators variable)
ERROR:    [RomM][init] Failed to run database migrations
```

This mainly affects external or managed database servers, because binary logging is on by default on MySQL 8 and is commonly enabled on hardened or replicated MariaDB instances. The `mariadb:11` container from the reference Compose is not affected out of the box.

Both fixes below have to be applied by an admin or root database user rather than the RomM user. The quickest one sets the global flag, though it is lost when the database restarts:

```sql
SET GLOBAL log_bin_trust_function_creators = 1;
```

To make it survive a restart, add it under `[mysqld]` in the server's option file and restart the database (see [Configuring MariaDB with option files](https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/configuring-mariadb/configuring-mariadb-with-option-files)). That file is usually `my.cnf`, or `custom.cnf` under `/config` on the linuxserver image:

```cnf
[mysqld]
log_bin_trust_function_creators = 1
```

Alternatively, grant the privilege to the RomM user itself:

```sql
GRANT BINLOG ADMIN ON *.* TO 'romm-user'@'%';  -- MariaDB 10.5+
GRANT SUPER ON *.* TO 'romm-user'@'%';         -- older MariaDB, or MySQL
```

Restart RomM once the change is in place. A migration that failed this way is safe to re-run, so it picks up from wherever it stopped and completes.

## PostgreSQL

```yaml
services:
    romm:
        environment:
            - ROMM_DB_DRIVER=postgresql
            - DB_PORT=5432
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

## Extra connection parameters

`DB_QUERY_JSON` takes a JSON blob of extra parameters appended to the connection string, e.g. for enabling TLS to an external DB, a longer connection timeout, or a non-default port:

```yaml
environment:
  - DB_QUERY_JSON={"ssl": "true", "connect_timeout": "5"}
```
