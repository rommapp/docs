---
title: Synology
description: Install RomM on a Synology NAS via Container Manager / Docker.
---

# Synology

## Looking for an opinionated guide?

[Marius Bogdan Lixandru](https://mariushosting.com/) maintains excellent Synology-focused guides with either MariaDB or Postgres:

- [How to Install RomM on Your Synology NAS (MariaDB)](https://mariushosting.com/how-to-install-romm-on-your-synology-nas/)
- [How to Install RomM With PostgreSQL on Your Synology NAS](https://mariushosting.com/how-to-install-romm-with-postgresql-on-your-synology-nas/)

Follow those if they match your setup. The walkthrough below is the fallback for everything else.

## Prerequisites

- A Synology NAS with Container Manager (DSM 7.2+) or the legacy Docker package.
- SSH or a task that lets you run shell commands on the NAS.
- Basic comfort with Docker Compose.

## 1. Create folders

RomM wants its data split across a few well-known paths. Do this once, via SSH:

### ROM library

```bash
mkdir -p /volume1/data/media/games/library/roms
mkdir -p /volume1/data/media/games/library/bios
```

The platform folder names inside `roms/` have to match RomM's conventions. See [Folder Structure](../getting-started/folder-structure.md).

### User uploads + config

```bash
mkdir -p /volume1/data/media/games/assets
mkdir -p /volume1/data/media/games/config
```

### Docker volumes for RomM itself

```bash
mkdir -p /volume1/docker/romm-project/
mkdir -p /volume1/docker/romm/resources
mkdir -p /volume1/docker/romm/redis-data
mkdir -p /volume1/docker/mariadb-romm
```

## 2. Create a bridge network

RomM and MariaDB need to reach each other by container name. Create a Docker bridge named `rommbridge`: [guide here](https://drfrankenstein.co.uk/step-3-setting-up-a-docker-bridge-network-in-container-manager/).

## 3. Generate the auth secret

```bash
openssl rand -hex 32
# -> 03a054b6ca27e0107c5eed552ea66bacd9f3a2a8a91e7595cd462a593f9ecd09
```

Keep the output. It becomes `ROMM_AUTH_SECRET_KEY` in your compose file. Don't lose it, because rotating invalidates every session and invite link.

## 4. Set up metadata provider credentials

Recommended before the first scan. Full walkthrough in [Metadata Providers](../administration/metadata-providers.md).

## 5. Docker Compose

!!! info "MariaDB 10.7 note"
    This guide pins MariaDB to **10.7** for stability on older DSM versions. MariaDB 11 works on DSM 7.2+, so bump the image tag if you like.

The Synology-flavoured compose file: MariaDB on port `3309` externally (to avoid colliding with Synology's built-in MariaDB), UID/GID customisation, simplified healthcheck:

???+ example "docker-compose.yml"
    ``` yaml
    --8<-- "synology.docker-compose.yml"
    ```

Replace placeholder UIDs, GIDs, passwords, API keys, and `ROMM_AUTH_SECRET_KEY` with your own before starting.

## 6. Launch

From the directory holding your compose file:

```bash
sudo docker compose up -d
```

**Be patient.** The first start takes a few minutes while MariaDB initialises, RomM runs migrations, and resources get seeded. Tail the logs:

```bash
sudo docker compose logs -f
```

Once RomM reports it's listening, open `http://<nas-ip>:7676` in a browser. The Setup Wizard walks you through creating the first admin.

## Notes

- **Permissions**: make sure the UID/GID in your compose file has read-write on every host path you mounted. Synology's default `docker` user is often `1024:100`, and the `apps` user is `568`. Pick one and be consistent.
- **HTTPS**: put Synology's built-in reverse proxy (Control Panel → Login Portal → Advanced → Reverse Proxy) in front of RomM, or use the [Reverse Proxy](reverse-proxy.md) recipes.
- **Back up `/volume1/docker/romm` and your DB volume** before upgrading RomM versions. See [Backup & Restore](backup-and-restore.md).

## Troubleshooting

Common Synology gotchas:

- **"Page not found" on first open**: DSM hit RomM before it finished first-run init. Wait for `docker compose logs -f` to calm down.
- **Database connection errors**: check the MariaDB container is healthy (`docker ps` → status `healthy`), and that RomM's `DB_HOST` matches the MariaDB service name in compose.
- **Permission errors on assets/resources folders**: verify the UID/GID in the compose matches the owner of those host paths on the NAS (`ls -la /volume1/data/media/games/`).

Synology-specific problems that come up often: [Synology Troubleshooting](../troubleshooting/synology.md).

## Contributing

Originally adapted from [ChopFoo's guide](https://github.com/rommapp/docs). Suggestions welcome via PR.
