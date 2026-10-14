---
title: Pethost
description: One-click deploy with Pethost's RomM template
---

# Pethost

[Pethost](https://pethost.dev/) is managed Docker hosting with one-click templates. Its RomM template runs the standard stack as a Docker Compose project, with an HTTPS address and nightly backups.

[![Deploy on Pethost](../resources/pethost/button.svg)](https://console.pethost.dev/?template=romm)

<!-- prettier-ignore -->
!!! note "Maintained by Pethost"
    Report template issues to [support@pethost.dev](mailto:support@pethost.dev).

## What it deploys

- **romm**: `rommapp/romm:5`, behind the project's HTTPS address. `REDIS_HOST` is unset, so the image starts its [embedded Valkey](redis-or-valkey.md).
- **db**: `mariadb:11.8`, reachable only inside the project

One named volume holds `/romm` (library, resources, assets and config), another `/redis-data`, and a third MariaDB's data. `ROMM_AUTH_SECRET_KEY` and the database passwords are generated at deploy and kept in the project's `.env`. `HASHEOUS_API_ENABLED` is on, as in the reference compose file.

## After deploy

1. Open the project's address and finish the first-boot setup wizard.
2. Place ROMs under `/romm/library` using a supported [folder structure](../getting-started/folder-structure.md), over SFTP or with an upload in RomM.
3. Add [metadata provider](../getting-started/metadata-providers.md) credentials to the project's `.env`, deploy again, then run a scan.
