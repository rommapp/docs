---
title: Backup & Restore
description: Protect your RomM install against data loss and move it between hosts.
---

# Backup & Restore

This page covers both routine backups and migrating RomM to a new host.

## What to back up

| Path / volume                                | What's in it                                                                                            | Backup?                                                                                                                      |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Database** (`mysql_data`, `pg_data`, etc.) | User accounts, ROM metadata, collections, ratings, play sessions, paired devices, saves/states metadata | **Critical**: back this up nightly.                                                                                          |
| **`/romm/assets`**                           | User uploads: save files, save states, user-uploaded screenshots, manuals, covers                       | **Critical**: back this up nightly.                                                                                          |
| **`/romm/config`**                           | `config.yml` and any custom overrides                                                                   | **Critical**: rarely changes, but small and painful to recreate.                                                             |
| `/romm/resources`                            | Metadata images (covers, screenshots) fetched from IGDB/ScreenScraper/etc.                              | Low priority, and can be re-downloaded on a rescan. Including it speeds up recovery.                                         |
| `/redis-data`                                | Task queue state                                                                                        | Low priority, in-flight tasks only, and lost tasks can be re-run.                                                            |
| **`/romm/library`**                          | Your ROM files                                                                                          | Back this up **separately**. It's your source data and you should already have a backup strategy for it independent of RomM. |

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

Offsite it however you already do (rclone to B2/S3, restic, borg, Proxmox Backup Server). RomM doesn't care.

## Restore

### Into an empty install

1. Start a fresh RomM stack with the same `ROMM_AUTH_SECRET_KEY` (if the secret changes, all sessions and invite links are invalidated). Point it at empty volumes.
2. Wait for the first-run setup to finish, then stop the stack: `docker compose stop`.
3. Restore the DB:
    ```sh
    docker exec -i romm-db mariadb --user=root --password=<root-pw> romm < romm-db-2026-04-15.sql
    # or for Postgres:
    docker exec -i romm-db psql --username=romm-user --dbname=romm < romm-db-2026-04-15.sql
    ```
4. Restore `assets/` and `config/` to the mounted host paths.
5. Restart: `docker compose start`. RomM will run any pending Alembic migrations automatically, so restoring a dump from an older version into a newer install is safe.

### In place (oh no, something's broken)

Same steps, but skip step 1. Stop the stack, swap the DB dump back in, restart. Keep the dump you're about to overwrite: `mv current-broken.sql rollback.sql`.

## Moving RomM to a new host

Same mechanics as a restore. Two approaches:

### Option A: logical dump + host-to-host copy (recommended)

Cleaner, version-independent, works across DB driver changes.

```sh
# on old host
docker exec romm-db mariadb-dump --user=romm-user --password=$DB_PASSWD \
  --single-transaction --databases romm > romm-db.sql
tar czf romm-data.tar.gz /srv/romm/assets /srv/romm/config

# transfer both files to the new host, then on the new host:
docker compose up -d romm-db                  # start DB container first
docker exec -i romm-db mariadb --user=root --password=$ROOT_PW romm < romm-db.sql
tar xzf romm-data.tar.gz -C /
docker compose up -d                          # start the rest
```

### Option B: Docker-volume copy

If you're lazy and on the same Docker version, copy volume data directly.

```sh
# on old host, stop RomM first
docker compose down

docker volume ls
# DRIVER    VOLUME NAME
# local     romm_mysql_data
# local     romm_romm_redis_data
# local     romm_romm_resources

docker volume inspect romm_mysql_data | grep Mountpoint
# "Mountpoint": "/var/lib/docker/volumes/romm_mysql_data/_data"

sudo rsync -aHAX /var/lib/docker/volumes/romm_mysql_data/    new-host:/opt/romm/mysql_data/
sudo rsync -aHAX /var/lib/docker/volumes/romm_romm_redis_data/ new-host:/opt/romm/redis_data/
sudo rsync -aHAX /var/lib/docker/volumes/romm_romm_resources/  new-host:/opt/romm/resources/

# on new host, bind-mount those paths instead of named volumes:
#   volumes:
#     - /opt/romm/mysql_data/_data:/var/lib/mysql
#     - /opt/romm/redis_data/_data:/redis-data
#     - /opt/romm/resources/_data:/romm/resources
```

Works, but binds you to matching the old host's Docker layout. Use Option A unless you have a reason not to.

## Verifying a backup is actually restorable

A backup you haven't restored is a hope, not a backup. Once a quarter, spin up a throwaway RomM stack from a recent backup:

```sh
# in a scratch directory
cp docker-compose.yml ./test-compose.yml
# point DB + assets volumes at test paths
docker compose -f test-compose.yml up -d
# restore the latest dump into it
# log in, check that users/collections/saves are present
docker compose -f test-compose.yml down -v
```

## Upgrade pre-flight

Before upgrading to a new RomM major version:

1. Stop the stack: `docker compose stop`.
2. Take a fresh DB dump (above).
3. Snapshot the assets + config volumes.
4. Start back up: `docker compose start`.
5. Pull the new image and upgrade.

If the upgrade blows up, restore the dump + snapshot. For 4.x → 5.0 specifically, read [Upgrading to 5.0](../releases/upgrading-to-5.0.md) first, because there are breaking changes.
