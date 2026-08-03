---
title: Railway
description: One-click deploy with a community-maintained Railway template
---

# Railway

The RomM team doesn't publish a first-party Railway template. A
**community-maintained** one-click option is available if you want a hosted
deploy without wiring Docker Compose yourself.

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/romm)

- Live template: <https://railway.com/deploy/romm>
- Template source (deployment config only): <https://github.com/osbytes/template-romm>

## What it deploys

The template runs the standard RomM stack as two Railway services:

- **app** — `rommapp/romm` (public). Leaves `REDIS_HOST` unset so the image
  starts its [embedded Valkey](redis-or-valkey.md).
- **mariadb** — MariaDB on private networking

Railway allows one volume per service. The template mounts `/romm` on `app`
(library, resources, assets, and config). `/redis-data` is ephemeral on
Railway.

## After deploy

1. Open the public **app** URL and finish the first-boot setup wizard.
2. Place ROMs under `/romm/library` using a supported
   [folder structure](../getting-started/folder-structure.md).
3. Optionally add [metadata provider](../getting-started/metadata-providers.md)
   credentials in the Railway service variables, then run a scan.

<!-- prettier-ignore -->
!!! note "Community-maintained"
    Report Railway-template issues to the [template maintainers](https://github.com/osbytes/template-romm/issues),
    not the main RomM issue tracker.
