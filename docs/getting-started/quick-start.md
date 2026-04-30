---
title: Quick Start
description: Get your instance running in about fifteen minutes
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# Quick Start

This guide gets a RomM instance up and running with the default stack (MariaDB + Valkey) using Docker Compose. If you're on Unraid, Synology, TrueNAS, or Kubernetes, check out the [Install & Deploy](../install/index.md) section for platform-specific guides.

## Before you start

You'll need:

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed on the host
- Your ROM files organised in the expected [folder structure](folder-structure.md)
- API credentials for at least one [metadata provider](../administration/metadata-providers.md)

<!-- prettier-ignore -->
!!! warning "Metadata providers are recommended"
    Scans work without a metadata API for basic use but setup problems and companion-app integrations (e.g. Playnite) can fail without them. Setting up **at least one** provider before your first scan is strongly recommended.

## 1. Write your `docker-compose.yml`

Start from the reference file shipped in the repo. A known-good, minimally-edited version is included below. Save it as `docker-compose.yml` in an empty directory on your host.

<!-- prettier-ignore -->
???+ example "docker-compose.yml"
    `yaml
        --8<-- "quick-start.docker-compose.yml"
    `

You'll want to edit the following values before launching:

| Where     | Variable                  | What to put                                                                                                            |
| --------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `romm-db` | `MARIADB_ROOT_PASSWORD`   | A long, randomly generated password.                                                                                   |
| `romm-db` | `MARIADB_PASSWORD`        | A separate long, randomly generated password.                                                                          |
| `romm`    | `DB_PASSWD`               | Must match `MARIADB_PASSWORD` above.                                                                                   |
| `romm`    | `ROMM_AUTH_SECRET_KEY`    | Generate with `openssl rand -hex 32` and keep it secret.                                                               |
| `romm`    | Metadata provider creds   | Fill in only the providers you've registered with (see [Metadata Providers](../administration/metadata-providers.md)). |
| `romm`    | `/path/to/library` volume | Host path to the directory containing your `roms/` folder.                                                             |
| `romm`    | `/path/to/assets` volume  | Host storage paths for saves, states and screenshots.                                                           |
| `romm`    | `/path/to/config` volume  | Host path to a directory that will hold `config.yml`.                                                                  |

Generate the auth secret now so you don't forget:

```sh
openssl rand -hex 32
# -> 03a054b6ca27e0107c5eed552ea66becd9f3a2a8a91e7595cd462a593f9ecd09
```

## 2. Start the stack

From the directory containing your `docker-compose.yml`:

```sh
docker compose up -d
```

On the first run Docker will pull `rommapp/romm:latest` and `mariadb:latest`, bring up the database, wait for the healthcheck, then bring up the app. Verify everything is running:

```sh
docker ps -f name=romm
```

```asciinema-player
    {
        "file": "../resources/asciinema/quick-start-docker-compose.cast",
        "title": "RomM docker compose install",
        "preload": true,
        "loop": true,
        "auto_play": true,
        "cols": 140,
        "rows": 30,
        "fit": "width",
        "terminal_font_size": "small",
        "terminal_line_height": "1.2",
        "terminal_font_family": "Roboto Mono, Monaco, Consolas, monospace"
    }
```

## 3. Create the admin user

Open `http://<host>:80` in a browser. On first start, you'll be redirected to the **Setup Wizard**. Set an admin username and password (the first user created always gets the Admin role), then log in.

## Next steps

- Populate the library by [scanning the mounted ROMs](first-scan.md)
- [Upload](../using/uploads.md) a handful of files in through the web UI
