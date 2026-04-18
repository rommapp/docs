---
title: Quick Start
description: Get a RomM 5.0 instance running in about fifteen minutes using Docker Compose.
---

# Quick Start

This guide gets a RomM instance up and running with the default stack (MariaDB + Valkey) using Docker Compose. If you're on Unraid, Synology, TrueNAS, or Kubernetes, start there instead: the [Install & Deploy](../install/index.md) section has platform-specific guides.

## Before you start

You'll need:

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed on the host.
- Your ROM files organised in the expected [folder structure](folder-structure.md).
- API credentials for at least one [metadata provider](../administration/metadata-providers.md). Hasheous + IGDB + SteamGridDB + Retroachievements is the recommended pairing. RomM will run without any provider configured, but matching quality will suffer.

!!! warning "Metadata providers are recommended"
    RomM works without a metadata API for basic use, but setup problems and companion-app integrations (e.g. Playnite) can fail without them. Setting up **IGDB**, **SteamGridDB**, and **Retroachievements** API keys before your first scan is strongly recommended.

## 1. Write your `docker-compose.yml`

Start from the reference file shipped in the RomM repo. A known-good, minimally-edited version is included below. Save it as `docker-compose.yml` in an empty directory on your host.

???+ example "docker-compose.yml"
    ``` yaml
    --8<-- "quick-start.docker-compose.yml"
    ```

You'll want to edit the following values before launching:

| Where | Variable | What to put |
| --- | --- | --- |
| `romm-db` | `MARIADB_ROOT_PASSWORD` | A long, randomly generated password. |
| `romm-db` | `MARIADB_PASSWORD` | A separate long, randomly generated password. |
| `romm` | `DB_PASSWD` | Must match `MARIADB_PASSWORD` above. |
| `romm` | `ROMM_AUTH_SECRET_KEY` | Generate with `openssl rand -hex 32` and keep it secret. |
| `romm` | Metadata provider creds | Fill in only the providers you've registered with (see [Metadata Providers](../administration/metadata-providers.md)). |
| `romm` | `/path/to/library` volume | Host path to the directory containing your `roms/` folder. |
| `romm` | `/path/to/assets` volume | Host path where RomM will store saves, states, uploaded screenshots. |
| `romm` | `/path/to/config` volume | Host path to a directory that will hold `config.yml`. |

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

On the first run Docker will pull `rommapp/romm:latest` and `mariadb:latest`, bring up the database, wait for the healthcheck, then start RomM. Verify everything is running:

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

Open `http://<host>:80` in a browser. The first time RomM starts, you'll be redirected to the **Setup Wizard**. Set an admin username and password (the first user created always gets the Admin role), then log in.

## 4. Scan your library

The fastest way to populate RomM is to let it scan your mounted library:

1. Click **Scan** in the sidebar.
2. Pick the metadata providers you configured in step 1.
3. Start the scan. You can open any matched game while the scan continues to see the metadata RomM pulled.
4. When the scan finishes, click the RomM logo to return home. You'll see your platforms and the most recently added games.

That's it, you're up and running! From here:

- Add more users and lock down access: [Users & Roles](../administration/users-and-roles.md)
- Put RomM behind a reverse proxy with HTTPS: [Reverse Proxy](../install/reverse-proxy.md)
- Learn what all those settings mean: [Core Concepts](concepts.md)

## Alternative: upload ROMs through the UI

If your library isn't mounted (yet) or you're just adding a handful of files, the upload dialog is fine for small batches. Not recommended for the initial import of a large collection, and it doesn't handle multi-file ROMs:

1. Click **Upload** in the sidebar.
2. Choose the target platform, click **+ ADD**, and select the files to upload.
3. Click **Upload** and wait for the transfer to finish.

<img src="https://raw.githubusercontent.com/rommapp/docs/refs/heads/main/docs/resources/quickstart/upload_roms.png" width="780" alt="upload dialog">
