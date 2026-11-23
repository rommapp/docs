---
title: Simafri
description: Run the reference Docker Compose stack on a Simafri managed VPS
---

# Simafri

[Simafri](https://www.simafri.com) publishes a [step-by-step guide](https://www.simafri.com/en/guides/self-host-romm/) for running RomM on its managed VPS with the [reference Docker Compose](../getting-started/quick-start.md) stack. Simafri handles the server's system updates, monitoring and encrypted nightly backups kept off the machine, while you keep root access and run the same `rommapp/romm` image documented everywhere else in these docs.

## What the guide deploys

The stack lives in `/opt/romm`:

- **romm**: `rommapp/romm:5.4.1`, with port `8080` published on `127.0.0.1:8102` only. `REDIS_HOST` is unset, so the image starts its [embedded Valkey](redis-or-valkey.md).
- **romm-db**: `mariadb:11.8`, reachable only inside the project.
- **Caddy**, as the [reverse proxy](reverse-proxy.md). It runs on the host under systemd and obtains a Let's Encrypt certificate for your domain.

The library, assets and config are directories under `/opt/romm`, while the database, resources and Valkey data persist in named volumes. `DB_PASSWD`, `MARIADB_ROOT_PASSWORD` and `ROMM_AUTH_SECRET_KEY` are generated into a `.env` file readable by root only, and `ROMM_BASE_URL` and `ROMM_SESSION_SECURE_COOKIE=true` are set for HTTPS.

## After install

1. Open your domain and finish the setup wizard, where the first account becomes the administrator.
2. Copy ROMs over SFTP into `/opt/romm/library/roms/<platform>` using a supported [folder structure](../getting-started/folder-structure.md), then run a scan (see [Your First Scan](../getting-started/first-scan.md)).
3. Add [metadata provider](../getting-started/metadata-providers.md) credentials to `/opt/romm/.env`, then run `docker compose up -d`.

The guide also covers backups with `mariadb-dump` and an archive of `/romm/assets`, `/romm/config` and `/romm/resources`, a restore into an emptied database, and updates by changing the image tag.
