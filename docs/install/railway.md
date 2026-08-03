---
title: Railway
description: One-click deploy with a community-maintained Railway template
---

# Railway

If you want a hosted deploy without wiring the Docker Compose yourself, a **community-maintained** one-click install option for Railway is available.

[![Deploy on Railway](../resources/railway/button.svg)](https://railway.com/deploy/romm)

<!-- prettier-ignore -->
!!! note "Community maintained"
    Report Railway template issues to the [template maintainers](https://github.com/osbytes/template-romm/issues).

## What it deploys

The template runs the standard stack as two Railway services:

- **app**: `rommapp/romm` (public), leaves `REDIS_HOST` unset so the image starts its [embedded Valkey](redis-or-valkey.md).
- **mariadb**: `mariadb` (private), MariaDB on private networking

Since Railway only allows one volume per service, the template mounts `/romm` on `app` (library, resources, assets, and config), and `/redis-data` is ephemeral.

## After deploy

1. Open the public **app** URL and finish the first-boot setup wizard.
2. Place ROMs under `/romm/library` using a supported [folder structure](../getting-started/folder-structure.md).
3. Add [metadata provider](../getting-started/metadata-providers.md) credentials in the Railway service variables, then run a scan.

The template source lives at [osbytes/template-romm](https://github.com/osbytes/template-romm).
