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
| **PostgreSQL**                     | `postgresql`     | `postgres:16` | `5432`       | Use if you already run Postgres.    |

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

`DB_QUERY_JSON` takes a JSON blob of extra parameters appended to the connection string. Useful for enabling TLS to an external DB, setting a connection timeout, or hitting a non-default port:

```yaml
environment:
  - DB_QUERY_JSON={"ssl": "true", "connect_timeout": "5"}
```
