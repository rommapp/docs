---
title: TrueNAS
description: Install on TrueNAS SCALE via the App Catalog or YAML
---

# TrueNAS

This guide covers **TrueNAS SCALE**. TrueNAS CORE isn't supported because its FreeBSD jail system doesn't run Docker images.

## Prerequisites

- A running TrueNAS SCALE installation
- Your library arranged in the expected [folder structure](../getting-started/folder-structure.md)
- A TrueNAS user/group with a UID/GID that can own the dataset paths you'll mount in

## Option A: App Catalog (recommended)

1. Open the RomM app

**Apps** (left nav) → **Discover Apps** → search `RomM` → **Install**.

![RomM app](../resources/truenas/appstore.png)

2. Fill in the install form

You'll be asked for the same set of env vars as [Quick Start](../getting-started/quick-start.md), and most defaults work. Things to look at:

- **Database credentials**: TrueNAS will offer to provision MariaDB for you, just pick a strong password.
- **`ROMM_AUTH_SECRET_KEY`**: generate via `openssl rand -hex 32` on any Linux box and paste the output.
- **Metadata provider credentials**: fill in whatever you've registered for (see [Metadata Providers](../administration/metadata-providers.md)).
- **Storage configurations**: point the **Library** and **Assets** volumes at datasets you control.
  - Make sure the UID/GID defined in the app config (default: `568`, the `apps` user) has ACL access to those datasets.

![RomM Library Example](../resources/truenas/app-config.png)

3. Install

Save, and TrueNAS will provision the container + DB + Valkey, run migrations, and expose the web UI on the port you configured. If it won't boot, jump to [Troubleshooting](#troubleshooting).

## Option B: Install via YAML

Use this path when the App Catalog has a bug, or when you want more flexibility than the install UI exposes.

1. Open the YAML install

**Apps** → **Discover Apps** → **Install via YAML**.

![Install via YAML](../resources/truenas/install-via-yaml.png)

2. Paste the compose file

Fill in the empty values with credentials you created in [Quick Start](../getting-started/quick-start.md).

<!-- prettier-ignore -->
???+ example "docker-compose.yml"
    `yaml
        --8<-- "truenas.docker-compose.yml"
    `

3. Install

Save, and you're done!

## Troubleshooting

### Generic

- Check you've filled in passwords and any required API keys (and UID/GID, if you're using the App Catalog form).
- Make sure the TrueNAS dataset permissions allow the chosen UID/GID to read/write.
- Watch the app's terminal / logs during startup for clues.

### Permission errors inside the container

If you're seeing permission errors on paths _inside_ the container (not on TrueNAS datasets), try temporarily running the container as root (`user: 0`) to unblock yourself, fix the offending permissions via shell, and switch back to a non-root user. In at least one reported setup, creating a user/group in TrueNAS with UID/GID `1000:1000` and the auxiliary `apps` group was needed to get the app talking to its embedded Valkey cleanly.

### Other issues

- [Scanning Troubleshooting](../troubleshooting/scanning.md) for matching / ingest problems
- [Authentication Troubleshooting](../troubleshooting/authentication.md) for login issues
- The [Discord](https://discord.gg/P5HtHnhUDH) has a `#truenas` channel with active community troubleshooting.
