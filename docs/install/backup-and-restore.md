---
title: Backup & Restore
description: Protect your install against data loss
---

# Backup & Restore

This page covers routine backups and restoring from them.

## What to back up

| Path / volume                                | What's in it                                                                                            | Backup?                                                                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Database** (`mysql_data`, `pg_data`, etc.) | User accounts, ROM metadata, collections, ratings, play sessions, paired devices, saves/states metadata | **Critical**: back this up nightly.                                                                      |
| **`/romm/assets`**                           | User uploads: save files, save states, user-uploaded screenshots, manuals, covers                       | **Critical**: back this up nightly.                                                                      |
| **`/romm/config`**                           | `config.yml` and any custom overrides                                                                   | **Critical**: rarely changes but small and painful to recreate.                                          |
| `/romm/resources`                            | Metadata images (covers, screenshots) fetched from IGDB/ScreenScraper/etc.                              | Medium priority, and can be re-downloaded on a rescan (including it speeds up recovery).                 |
| `/redis-data`                                | Task queue state                                                                                        | Low priority, in-flight tasks only, and lost tasks can be re-run.                                        |
| **`/romm/library`**                          | Your ROM files                                                                                          | Back this up **separately**. It's your source data and you should already have a backup strategy for it. |

## Routine backup

<!-- prettier-ignore -->
!!! warning "Always stop the stack or use consistent snapshots"
    A live `cp -r` of the DB volume can copy an inconsistent state. Either bring the stack down briefly, or use `mysqldump` / `pg_dump` for a consistent logical dump.

### DB dump (MariaDB / MySQL)

```sh
docker exec romm-db mariadb-dump \
  --user=romm-user --password=<DB_PASSWD> \
  --single-transaction --databases romm \
  > romm-db-$(date +%F).sql
```

### DB dump (PostgreSQL)

```sh
docker exec romm-db pg_dump \
  --username=romm-user --dbname=romm \
  > romm-db-$(date +%F).sql
```

### Assets + config

Copy the host paths you mounted as `/romm/assets` and `/romm/config`. Incremental rsync is fine:

```sh
rsync -a --delete /srv/romm/assets/ /backup/romm/assets/
rsync -a --delete /srv/romm/config/ /backup/romm/config/
```

### Putting it together

A minimal nightly cron:

```sh
#!/usr/bin/env bash
set -euo pipefail
STAMP=$(date +%F)
DEST=/backup/romm

docker exec romm-db mariadb-dump --user=romm-user --password=$DB_PASSWD \
  --single-transaction --databases romm | gzip > "$DEST/db-$STAMP.sql.gz"

rsync -a --delete /srv/romm/assets/ "$DEST/assets/"
rsync -a --delete /srv/romm/config/ "$DEST/config/"

# keep 14 days of DB dumps
find "$DEST" -maxdepth 1 -name 'db-*.sql.gz' -mtime +14 -delete
```

Send it offsite however you already do (rclone to B2/S3, restic, borg). Rememer the 3-2-1 rule: 3 copies, on 2 different media, with 1 offsite!

## Restore

### Into an empty install

1. Start a fresh stack with the same `ROMM_AUTH_SECRET_KEY` (if the secret changes, all sessions and invite links are invalidated).
2. Wait for the first-run setup to finish, then stop the stack: `docker compose stop`.
3. Restore the DB:
  ```sh
  docker exec -i romm-db mariadb --user=root --password=<root-pw> romm < romm-db-2026-04-15.sql
  # or for Postgres:
  docker exec -i romm-db psql --username=romm-user --dbname=romm < romm-db-2026-04-15.sql
  ```
4. Restore `assets/`, `config/` and `resources/` to the mounted host paths.
5. Restart with `docker compose start`.

## Verifying a backup is actually restorable

A backup you haven't restored is a hope, not a backup. Spin up a throwaway stack from a recent backup twice a year:

```sh
# in a scratch directory
cp docker-compose.yml ./test-compose.yml
# point DB + assets volumes at test paths
docker compose -f test-compose.yml up -d
# restore the latest dump into it
# log in, check that users/collections/saves are present
docker compose -f test-compose.yml down -v
```
